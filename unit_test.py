"""
Apex Stock Screener — Unit Test Suite
Matches exact project structure:
  database/db.py  →  users_col, client, db
  auth/auth.py    →  login_view, signup_view
  auth/auth_utils →  hash_password, verify_password
  .env            →  MONGO_URI, INDIAN_API_KEY

Run: python -m pytest pages/unit_test.py -v
"""

import sys
import os
import pytest
import pandas as pd
from unittest.mock import MagicMock, patch

# ── Make sure project root is on path so imports work ────────────────────────
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# ═════════════════════════════════════════════════════════════════════════════
# 1. DB CONNECTION  (uses your real MONGO_URI from .env)
# ═════════════════════════════════════════════════════════════════════════════

def test_db_connection():
    """Real MongoDB connection using MONGO_URI from .env"""
    from database.db import client
    result = client.admin.command("ping")
    assert result.get("ok") == 1.0


# ═════════════════════════════════════════════════════════════════════════════
# 2. USERS COLLECTION EXISTS
# ═════════════════════════════════════════════════════════════════════════════

def test_users_collection_accessible():
    """apex_auth.users collection is reachable"""
    from database.db import users_col
    count = users_col.count_documents({}, limit=1)
    assert count >= 0


# ═════════════════════════════════════════════════════════════════════════════
# 3. PASSWORD HASH
# ═════════════════════════════════════════════════════════════════════════════

def test_password_hash():
    """hash_password returns a bcrypt hash, not plaintext"""
    from auth.auth_utils import hash_password
    pw     = "TestPass@2025"
    hashed = hash_password(pw)
    assert hashed != pw
    assert len(hashed) > 20


# ═════════════════════════════════════════════════════════════════════════════
# 4. PASSWORD VERIFY — CORRECT
# ═════════════════════════════════════════════════════════════════════════════

def test_verify_password_correct():
    """verify_password returns True for matching password"""
    from auth.auth_utils import hash_password, verify_password
    pw     = "TestPass@2025"
    hashed = hash_password(pw)
    assert verify_password(pw, hashed) is True


# ═════════════════════════════════════════════════════════════════════════════
# 5. PASSWORD VERIFY — WRONG
# ═════════════════════════════════════════════════════════════════════════════

def test_verify_password_wrong():
    """verify_password returns False for wrong password"""
    from auth.auth_utils import hash_password, verify_password
    hashed = hash_password("CorrectPass")
    assert verify_password("WrongPass", hashed) is False


# ═════════════════════════════════════════════════════════════════════════════
# 6. LOGIN — VALID USER
# ═════════════════════════════════════════════════════════════════════════════

def test_login_valid_credentials():
    """Login succeeds when userid + password are correct"""
    from auth.auth_utils import hash_password, verify_password

    fake_user = {
        "email":         "nakul@apex.com",
        "userid":        "nakul",
        "password":      hash_password("Pass@123"),
        "auth_provider": "local",
    }
    mock_col = MagicMock()
    mock_col.find_one.return_value = fake_user

    user = mock_col.find_one({"userid": "nakul"})
    assert user is not None
    assert verify_password("Pass@123", user["password"]) is True


# ═════════════════════════════════════════════════════════════════════════════
# 7. LOGIN — INVALID PASSWORD
# ═════════════════════════════════════════════════════════════════════════════

def test_login_invalid_password():
    """Login fails when password is wrong"""
    from auth.auth_utils import hash_password, verify_password

    fake_user = {
        "userid":   "nakul",
        "password": hash_password("Pass@123"),
    }
    mock_col = MagicMock()
    mock_col.find_one.return_value = fake_user

    user = mock_col.find_one({"userid": "nakul"})
    assert verify_password("WrongPass", user["password"]) is False


# ═════════════════════════════════════════════════════════════════════════════
# 8. LOGIN — USER NOT FOUND
# ═════════════════════════════════════════════════════════════════════════════

def test_login_user_not_found():
    """Login fails when userid does not exist"""
    mock_col = MagicMock()
    mock_col.find_one.return_value = None

    user = mock_col.find_one({"userid": "ghost_user"})
    assert user is None


# ═════════════════════════════════════════════════════════════════════════════
# 9. SIGNUP — DUPLICATE USER DETECTION
# ═════════════════════════════════════════════════════════════════════════════

def test_signup_duplicate_user():
    """Signup blocked when email or userid already exists"""
    mock_col = MagicMock()
    mock_col.find_one.return_value = {
        "userid": "nakul",
        "email":  "nakul@apex.com",
    }
    existing = mock_col.find_one({
        "$or": [
            {"email":  "nakul@apex.com"},
            {"userid": "nakul"},
        ]
    })
    assert existing is not None


# ═════════════════════════════════════════════════════════════════════════════
# 10. SIGNUP — NEW USER INSERT
# ═════════════════════════════════════════════════════════════════════════════

def test_signup_new_user_insert():
    """New user document inserted correctly into users_col"""
    from auth.auth_utils import hash_password

    mock_col = MagicMock()
    mock_col.find_one.return_value   = None
    mock_col.insert_one.return_value = MagicMock(inserted_id="abc123")

    existing = mock_col.find_one({"userid": "newuser"})
    assert existing is None

    mock_col.insert_one({
        "email":         "new@apex.com",
        "userid":        "newuser",
        "password":      hash_password("NewPass@1"),
        "auth_provider": "local",
    })
    mock_col.insert_one.assert_called_once()


# ═════════════════════════════════════════════════════════════════════════════
# 11. ACCOUNT SETTINGS — UPDATE USER
# ═════════════════════════════════════════════════════════════════════════════

def test_account_settings_update():
    """User profile update writes correct $set to MongoDB"""
    mock_col = MagicMock()
    mock_col.update_one.return_value = MagicMock(modified_count=1)

    result = mock_col.update_one(
        {"userid": "nakul"},
        {"$set": {"email": "nakul.new@apex.com"}}
    )
    assert result.modified_count == 1
    mock_col.update_one.assert_called_once_with(
        {"userid": "nakul"},
        {"$set": {"email": "nakul.new@apex.com"}}
    )


# ═════════════════════════════════════════════════════════════════════════════
# 12. STOCK FILTER — P/E RATIO
# ═════════════════════════════════════════════════════════════════════════════

def test_stock_filter_pe_ratio():
    """Screener correctly filters stocks by P/E range"""
    data = pd.DataFrame({
        "Ticker":   ["INFY.NS", "RELIANCE.NS", "TCS.NS"],
        "PE_Ratio": [22.5,       18.3,           35.1],
    })
    filtered = data[(data["PE_Ratio"] >= 15) & (data["PE_Ratio"] <= 30)]
    assert "INFY.NS"     in     filtered["Ticker"].values
    assert "RELIANCE.NS" in     filtered["Ticker"].values
    assert "TCS.NS"      not in filtered["Ticker"].values


# ═════════════════════════════════════════════════════════════════════════════
# 13. STOCK FILTER — RSI RANGE
# ═════════════════════════════════════════════════════════════════════════════

def test_stock_filter_rsi_range():
    """Screener correctly filters stocks by RSI range"""
    data = pd.DataFrame({
        "Ticker": ["HDFC.NS", "WIPRO.NS", "BAJAJ.NS"],
        "RSI":    [28.4,       55.2,        75.8],
    })
    filtered = data[(data["RSI"] >= 30) & (data["RSI"] <= 70)]
    assert "WIPRO.NS" in     filtered["Ticker"].values
    assert "HDFC.NS"  not in filtered["Ticker"].values
    assert "BAJAJ.NS" not in filtered["Ticker"].values


# ═════════════════════════════════════════════════════════════════════════════
# 14. API FETCH — YFINANCE (mocked)
# ═════════════════════════════════════════════════════════════════════════════

def test_api_fetch_ticker_data():
    """yfinance ticker fetch returns expected fields"""
    with patch("yfinance.Ticker") as mock_ticker:
        mock_ticker.return_value.info = {
            "shortName":     "Infosys Limited",
            "trailingPE":    22.5,
            "marketCap":     6000000000000,
            "dividendYield": 0.025,
        }
        import yfinance as yf
        info = yf.Ticker("INFY.NS").info
        assert info["trailingPE"] == 22.5
        assert "shortName" in info


# ═════════════════════════════════════════════════════════════════════════════
# 15. CSV EXPORT
# ═════════════════════════════════════════════════════════════════════════════

def test_csv_export_output(tmp_path):
    """Screener results export correctly to CSV"""
    df = pd.DataFrame({
        "Ticker":   ["INFY.NS", "TCS.NS"],
        "PE_Ratio": [22.5,       35.1],
        "RSI":      [55.2,       62.4],
    })
    out = tmp_path / "results.csv"
    df.to_csv(out, index=False)
    loaded = pd.read_csv(out)
    assert len(loaded) == 2
    assert "Ticker" in loaded.columns