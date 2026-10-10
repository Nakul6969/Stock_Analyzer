import requests
import numpy as np
import joblib
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY  = os.getenv("INDIAN_API_KEY")
BASE_URL = "https://stock.indianapi.in/stock"
HEADERS  = {"X-Api-Key": API_KEY}
MODEL_PATH = "ml/risk_model.pkl"


def get_metric(metrics_list, key):
    for item in metrics_list:
        if item.get("key") == key:
            v = item.get("value")
            return float(v) if v else None
    return None


def get_dma(technical_data, days):
    for item in technical_data:
        if item.get("days") == days:
            v = item.get("nsePrice")
            return float(v) if v else None
    return None


def get_price_metric(pv_list, key):
    for item in pv_list:
        if item.get("key") == key:
            v = item.get("value")
            return float(v) if v else None
    return None


_CACHED_MODEL_BUNDLE = None

def get_risk_model():
    """Load and cache the trained ML model bundle in memory to avoid redundant disk I/O."""
    global _CACHED_MODEL_BUNDLE
    if _CACHED_MODEL_BUNDLE is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("❌ Model not found. Run ml/train_model.py first.")
        _CACHED_MODEL_BUNDLE = joblib.load(MODEL_PATH)
    return _CACHED_MODEL_BUNDLE


def fetch_and_predict(stock_name: str) -> dict:
    """Fetch stock data from API and predict risk score."""

    # ── Load model (cached in memory) ──
    saved    = get_risk_model()
    model    = saved["model"]
    features = saved["features"]
    std_min  = saved["std_min"]
    std_max  = saved["std_max"]

    # ── Fetch from API ──
    resp = requests.get(
        BASE_URL,
        headers=HEADERS,
        params={"name": stock_name},
        timeout=10
    )

    if resp.status_code != 200:
        raise Exception(f"API error: {resp.status_code}")

    data = resp.json()

    # ── Extract features ──
    current_price = float(data.get("currentPrice", {}).get("NSE", 0) or 0)
    year_high     = float(data.get("yearHigh", current_price) or current_price)
    year_low      = float(data.get("yearLow",  current_price) or current_price)
    volatility    = (year_high - year_low) / year_low if year_low > 0 else 0

    tech       = data.get("stockTechnicalData", [])
    dma_50     = get_dma(tech, 50)
    dma_100    = get_dma(tech, 100)
    dma50_ratio  = current_price / dma_50  if dma_50  and dma_50  > 0 else 1.0
    dma100_ratio = current_price / dma_100 if dma_100 and dma_100 > 0 else 1.0

    km  = data.get("keyMetrics", {})
    pv  = km.get("priceandVolume", [])
    val = km.get("valuation", [])
    fs  = km.get("financialstrength", [])
    mg  = km.get("margins", [])
    gr  = km.get("growth", [])

    feature_values = {
        "volatility":      volatility,
        "beta":            get_price_metric(pv, "beta") or 1.0,
        "pe_ratio":        get_metric(val, "pPerEExcludingExtraordinaryItemsMostRecentFiscalYear") or 20.0,
        "price_to_book":   get_metric(val, "priceToBookMostRecentFiscalYear") or 2.0,
        "peg_ratio":       get_metric(val, "pegRatio") or 2.0,
        "debt_equity":     get_metric(fs, "totalDebtPerTotalEquityMostRecentFiscalYear") or 0.5,
        "current_ratio":   get_metric(fs, "currentRatioMostRecentFiscalYear") or 1.0,
        "lt_debt":         get_metric(fs, "ltDebtPerEquityMostRecentFiscalYear)") or 0.3,
        "op_margin":       get_metric(mg, "operatingMarginTrailing12Month") or 10.0,
        "net_margin":      get_metric(mg, "netProfitMarginPercentTrailing12Month") or 8.0,
        "gross_margin":    get_metric(mg, "grossMarginTrailing12Month") or 25.0,
        "eps_growth":      get_metric(gr, "ePSGrowthRate5Year") or 10.0,
        "revenue_growth":  get_metric(gr, "revenueGrowthRate5Year") or 8.0,
        "dma50_ratio":     dma50_ratio,
        "dma100_ratio":    dma100_ratio,
        "price_52w_change": get_price_metric(pv, "price52WeekPricePercentChange") or 0.0,
        "price_13w_change": get_price_metric(pv, "price13WeekPricePercentChange") or 0.0,
    }

    X = [[feature_values[f] for f in features]]

    # ── Predict ──
    raw_score = float(model.predict(X)[0])
    score     = round(float(np.clip(raw_score, 1, 10)), 1)

    # ── API's own risk label ──
    api_risk = data.get("riskMeter", {})
    api_label = api_risk.get("categoryName", "Unknown")
    api_std   = api_risk.get("stdDev", 0)

    # ── Risk label from our model ──
    if score <= 3:
        label = "Low Risk"
        color = "#22c55e"
        emoji = "🟢"
    elif score <= 6:
        label = "Medium Risk"
        color = "#f59e0b"
        emoji = "🟡"
    else:
        label = "High Risk"
        color = "#ef4444"
        emoji = "🔴"

    # ── Signal pills ──
    signals = []
    fv = feature_values
    if dma50_ratio  > 1: signals.append(("Above 50 DMA",  "ok"))
    else:                signals.append(("Below 50 DMA",  "warn"))
    if dma100_ratio > 1: signals.append(("Above 100 DMA", "ok"))
    else:                signals.append(("Below 100 DMA", "warn"))
    if fv["pe_ratio"] > 30: signals.append(("High PE ratio", "warn"))
    else:                   signals.append(("Healthy PE",    "ok"))
    if fv["beta"] > 1.2:    signals.append(("High beta",     "warn"))
    else:                   signals.append(("Stable beta",   "ok"))
    if fv["debt_equity"] > 1: signals.append(("High debt",   "warn"))
    else:                     signals.append(("Low debt",     "ok"))
    if fv["net_margin"] > 10: signals.append(("Strong margins", "ok"))
    else:                     signals.append(("Thin margins",   "warn"))

    return {
        "stock_name":    data.get("companyName", stock_name),
        "ticker":        data.get("tickerId", stock_name.upper()),
        "score":         score,
        "label":         label,
        "color":         color,
        "emoji":         emoji,
        "signals":       signals,
        "features":      feature_values,
        "api_risk_label": api_label,
        "api_std_dev":   api_std,
        "current_price": current_price,
        "year_high":     year_high,
        "year_low":      year_low,
        "dma_50":        dma_50,
        "dma_100":       dma_100,
    }
