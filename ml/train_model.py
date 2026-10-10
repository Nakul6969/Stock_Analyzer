import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import os
from dotenv import load_dotenv
import time

load_dotenv()

API_KEY = os.getenv("INDIAN_API_KEY")
BASE_URL = "https://stock.indianapi.in/stock"
HEADERS  = {"X-Api-Key": API_KEY}

# ── Stocks to train on ────────────────────────────────
STOCKS = [
    "Reliance", "TCS", "Infosys", "HDFC Bank", "ICICI Bank",
    "Wipro", "HCL Technologies", "Bajaj Finance", "Maruti Suzuki",
    "Tata Motors", "SBI", "Axis Bank", "Kotak Bank", "LTIMindtree",
    "Sun Pharma", "Adani Ports", "Asian Paints", "Titan", "Nestle",
    "Hindustan Unilever", "ONGC", "Power Grid", "NTPC", "Coal India",
    "Bharti Airtel", "Tata Steel", "JSW Steel", "Hindalco", "UltraTech",
    "Divi Labs", "Bajaj Auto", "Hero MotoCorp", "Eicher Motors",
    "Havells", "Pidilite", "Cipla", "Dr Reddy", "Lupin",
    "Apollo Hospitals", "Zomato", "Tata Power", "Adani Green",
    "Bank of Baroda", "Punjab National Bank", "Canara Bank",
    "Federal Bank", "Yes Bank", "IDFC First Bank",
    "Muthoot Finance", "Tech Mahindra", "Mphasis", "Persistent",
    "Coforge", "Bharat Forge", "Cummins India", "ABB India",
    "Siemens", "DLF", "Godrej Properties", "ITC", "Britannia",
    "Dabur", "Marico", "Colgate", "Tata Consumer", "Varun Beverages",
    "Torrent Pharma", "Aurobindo", "Fortis Healthcare",
    "Indus Towers", "RBL Bank", "Cholamandalam", "Shriram Finance",
]

# ── Helper: extract value from keyMetrics list ────────
def get_metric(metrics_list, key):
    for item in metrics_list:
        if item.get("key") == key:
            v = item.get("value")
            return float(v) if v else None
    return None

# ── Helper: get DMA price ─────────────────────────────
def get_dma(technical_data, days):
    for item in technical_data:
        if item.get("days") == days:
            v = item.get("nsePrice")
            return float(v) if v else None
    return None

# ── Helper: get priceAndVolume metric ─────────────────
def get_price_metric(pv_list, key):
    for item in pv_list:
        if item.get("key") == key:
            v = item.get("value")
            return float(v) if v else None
    return None

# ── Fetch & extract features for one stock ────────────
def fetch_stock_features(stock_name):
    try:
        resp = requests.get(
            BASE_URL,
            headers=HEADERS,
            params={"name": stock_name},
            timeout=10
        )
        if resp.status_code != 200:
            print(f"  ❌ {stock_name}: status {resp.status_code}")
            return None

        data = resp.json()

        # ── Target: stdDev from riskMeter ──
        risk_meter = data.get("riskMeter", {})
        std_dev    = risk_meter.get("stdDev")
        if std_dev is None:
            print(f"  ⚠️ {stock_name}: no stdDev")
            return None
        std_dev = float(std_dev)

        # ── Current price ──
        current_price = float(data.get("currentPrice", {}).get("NSE", 0) or 0)
        if current_price == 0:
            return None

        # ── Year high / low ──
        year_high = float(data.get("yearHigh", current_price) or current_price)
        year_low  = float(data.get("yearLow",  current_price) or current_price)

        # ── Volatility: (high - low) / low ──
        volatility = (year_high - year_low) / year_low if year_low > 0 else 0

        # ── Technical data (DMAs) ──
        tech = data.get("stockTechnicalData", [])
        dma_50  = get_dma(tech, 50)
        dma_100 = get_dma(tech, 100)

        dma50_ratio  = current_price / dma_50  if dma_50  and dma_50  > 0 else 1.0
        dma100_ratio = current_price / dma_100 if dma_100 and dma_100 > 0 else 1.0

        # ── Price & volume metrics ──
        pv = data.get("keyMetrics", {}).get("priceandVolume", [])
        beta             = get_price_metric(pv, "beta")
        price_52w_change = get_price_metric(pv, "price52WeekPricePercentChange")
        price_13w_change = get_price_metric(pv, "price13WeekPricePercentChange")

        # ── Valuation ──
        val = data.get("keyMetrics", {}).get("valuation", [])
        pe_ratio      = get_metric(val, "pPerEExcludingExtraordinaryItemsMostRecentFiscalYear")
        price_to_book = get_metric(val, "priceToBookMostRecentFiscalYear")
        peg_ratio     = get_metric(val, "pegRatio")

        # ── Financial strength ──
        fs = data.get("keyMetrics", {}).get("financialstrength", [])
        debt_equity   = get_metric(fs, "totalDebtPerTotalEquityMostRecentFiscalYear")
        current_ratio = get_metric(fs, "currentRatioMostRecentFiscalYear")
        lt_debt       = get_metric(fs, "ltDebtPerEquityMostRecentFiscalYear")

        # ── Margins ──
        margins = data.get("keyMetrics", {}).get("margins", [])
        op_margin     = get_metric(margins, "operatingMarginTrailing12Month")
        net_margin    = get_metric(margins, "netProfitMarginPercentTrailing12Month")
        gross_margin  = get_metric(margins, "grossMarginTrailing12Month")

        # ── Growth ──
        growth = data.get("keyMetrics", {}).get("growth", [])
        eps_growth     = get_metric(growth, "ePSGrowthRate5Year")
        revenue_growth = get_metric(growth, "revenueGrowthRate5Year")

        # Clip extreme values
        return {
            "stock": stock_name,
            "std_dev": std_dev,
            "volatility": min(volatility, 2.0),  # cap at 200%
            "beta": min(abs(beta or 1.0), 3.0),  # cap at 3
            "pe_ratio": min(abs(pe_ratio or 20.0), 100),  # cap at 100
            "price_to_book": min(price_to_book or 2.0, 20),
            "peg_ratio": min(abs(peg_ratio or 2.0), 10),
            "debt_equity": min(abs(debt_equity or 0.5), 5),
            "current_ratio": min(current_ratio or 1.0, 10),
            "lt_debt": min(abs(lt_debt or 0.3), 5),
            "op_margin": op_margin or 10.0,
            "net_margin": net_margin or 8.0,
            "gross_margin": gross_margin or 25.0,
            "eps_growth": min(abs(eps_growth or 10.0), 100),
            "revenue_growth": min(abs(revenue_growth or 8.0), 100),
            "dma50_ratio": dma50_ratio,
            "dma100_ratio": dma100_ratio,
            "price_52w_change": price_52w_change or 0.0,
            "price_13w_change": price_13w_change or 0.0,
        }
    except Exception as e:
        print(f"  ❌ {stock_name}: {e}")
        return None


# ── Main training pipeline ────────────────────────────
def train():
    print("📦 Fetching stock data from IndianAPI.in...")
    records = []

    for stock in STOCKS:
        print(f"  Fetching {stock}...")
        result = fetch_stock_features(stock)
        if result:
            records.append(result)
            print(f"  ✅ {stock}: stdDev={result['std_dev']}")
        time.sleep(0.5)  # avoid rate limiting

    if len(records) < 5:
        print("❌ Not enough data to train. Check API key or stock names.")
        return

    df = pd.DataFrame(records)
    print(f"\n✅ Collected {len(df)} stocks for training")
    print(df[["stock", "std_dev"]].to_string())

    # ── Convert stdDev → risk score 1-10 ──
    # stdDev range roughly 5-40 for Indian stocks
    df["risk_score"] = ((df["std_dev"] - df["std_dev"].min()) /
                        (df["std_dev"].max() - df["std_dev"].min()) * 9 + 1).clip(1, 10)

    # ── Features ──
    FEATURES = [
        "volatility", "beta", "pe_ratio", "price_to_book",
        "peg_ratio", "debt_equity", "current_ratio", "lt_debt",
        "op_margin", "net_margin", "gross_margin",
        "eps_growth", "revenue_growth",
        "dma50_ratio", "dma100_ratio",
        "price_52w_change", "price_13w_change"
    ]

    X = df[FEATURES].fillna(df[FEATURES].median())
    y = df["risk_score"]

    # ── Clip extreme outliers ──
    X = X.clip(lower=X.quantile(0.05), upper=X.quantile(0.95), axis=1)

    # ── Train model ──
    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=4,
        min_samples_split=3,
        min_samples_leaf=2,
        random_state=42
    )

    # ── Cross validation (better evaluation for small datasets) ──
    cv_folds = min(5, len(df) // 5)  # adjust folds based on data size
    if cv_folds >= 3:
        cv_scores = cross_val_score(
            model, X, y,
            cv=cv_folds,
            scoring="neg_root_mean_squared_error"
        )
        print(f"\n📊 Cross-validation RMSE: {-cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        r2_scores = cross_val_score(model, X, y, cv=cv_folds, scoring="r2")
        print(f"📊 Cross-validation R²:   {r2_scores.mean():.3f} ± {r2_scores.std():.3f}")

    # ── Final train on ALL data ──
    model.fit(X, y)

    # Train score
    train_preds = model.predict(X)
    train_rmse = np.sqrt(mean_squared_error(y, train_preds))
    train_r2 = r2_score(y, train_preds)
    print(f"\n📊 Training Performance:")
    print(f"   RMSE : {train_rmse:.3f}")
    print(f"   R²   : {train_r2:.3f}")

    # ── Feature importance ──
    importance = pd.Series(model.feature_importances_, index=FEATURES)
    print(f"\n🔍 Top features:")
    print(importance.sort_values(ascending=False).head(8).to_string())

    # ── Save ──
    os.makedirs("ml", exist_ok=True)
    joblib.dump({
        "model":    model,
        "features": FEATURES,
        "std_min":  df["std_dev"].min(),
        "std_max":  df["std_dev"].max(),
    }, "ml/risk_model.pkl")

    print(f"\n✅ Model saved to ml/risk_model.pkl")
    print(f"   Trained on {len(X)} stocks")


if __name__ == "__main__":
    train()
