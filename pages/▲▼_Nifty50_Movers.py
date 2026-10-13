import streamlit as st
import requests
import os
from dotenv import load_dotenv
from ui.sidebar import render_sidebar
from ui.styles import load_global_css

import yfinance as yf
import pandas as pd
import json

# ======================================================
# PAGE CONFIG (MUST BE FIRST)

st.set_page_config(
    page_title="Apex Stock Screener | Nifty 50 Movers",
    page_icon="icon.png",
    layout="wide"
)
# Login Logic -----------------------------------------

if not st.session_state.get("logged_in"):
    st.switch_page("合_Welcome.py")

load_global_css()
render_sidebar()

# ======================================================
# ENV & API

load_dotenv()
API_KEY = os.getenv("INDIAN_API_KEY")
BASE_URL = "https://stock.indianapi.in"
HEADERS = {"X-Api-Key": API_KEY}

# ======================================================
# NIFTY 50 UNIVERSE (STRICT 50 CONSTITUENTS)
# ======================================================
NIFTY_50_STOCKS = {
    "ADANIENT": {"name": "Adani Enterprises", "sector": "Energy"},
    "ADANIPORTS": {"name": "Adani Ports", "sector": "Infrastructure"},
    "APOLLOHOSP": {"name": "Apollo Hospitals", "sector": "Healthcare"},
    "ASIANPAINT": {"name": "Asian Paints", "sector": "FMCG"},
    "AXISBANK": {"name": "Axis Bank", "sector": "Banking"},
    "BAJAJ-AUTO": {"name": "Bajaj Auto", "sector": "Auto"},
    "BAJFINANCE": {"name": "Bajaj Finance", "sector": "Finance"},
    "BAJAJFINSV": {"name": "Bajaj Finserv", "sector": "Finance"},
    "BEL": {"name": "Bharat Electronics", "sector": "Defence"},
    "BHARTIARTL": {"name": "Bharti Airtel", "sector": "Telecom"},
    "BPCL": {"name": "BPCL", "sector": "Energy"},
    "BRITANNIA": {"name": "Britannia Industries", "sector": "FMCG"},
    "CIPLA": {"name": "Cipla", "sector": "Pharma"},
    "COALINDIA": {"name": "Coal India", "sector": "Energy"},
    "DRREDDY": {"name": "Dr. Reddy's Laboratories", "sector": "Pharma"},
    "EICHERMOT": {"name": "Eicher Motors", "sector": "Auto"},
    "GRASIM": {"name": "Grasim Industries", "sector": "Materials"},
    "HCLTECH": {"name": "HCL Technologies", "sector": "IT"},
    "HDFCBANK": {"name": "HDFC Bank", "sector": "Banking"},
    "HDFCLIFE": {"name": "HDFC Life", "sector": "Insurance"},
    "HEROMOTOCO": {"name": "Hero MotoCorp", "sector": "Auto"},
    "HINDALCO": {"name": "Hindalco Industries", "sector": "Metals"},
    "HINDUNILVR": {"name": "Hindustan Unilever", "sector": "FMCG"},
    "ICICIBANK": {"name": "ICICI Bank", "sector": "Banking"},
    "ITC": {"name": "ITC Limited", "sector": "FMCG"},
    "INDUSINDBK": {"name": "IndusInd Bank", "sector": "Banking"},
    "INFY": {"name": "Infosys", "sector": "IT"},
    "JSWSTEEL": {"name": "JSW Steel", "sector": "Metals"},
    "KOTAKBANK": {"name": "Kotak Mahindra Bank", "sector": "Banking"},
    "LT": {"name": "Larsen & Toubro", "sector": "Infrastructure"},
    "M&M": {"name": "Mahindra & Mahindra", "sector": "Auto"},
    "MARUTI": {"name": "Maruti Suzuki", "sector": "Auto"},
    "NESTLEIND": {"name": "Nestle India", "sector": "FMCG"},
    "NTPC": {"name": "NTPC", "sector": "Energy"},
    "ONGC": {"name": "ONGC", "sector": "Energy"},
    "POWERGRID": {"name": "Power Grid Corporation", "sector": "Energy"},
    "RELIANCE": {"name": "Reliance Industries", "sector": "Energy"},
    "SBILIFE": {"name": "SBI Life", "sector": "Insurance"},
    "SBIN": {"name": "State Bank of India", "sector": "Banking"},
    "SUNPHARMA": {"name": "Sun Pharma", "sector": "Pharma"},
    "TCS": {"name": "Tata Consultancy Services", "sector": "IT"},
    "TATACONSUM": {"name": "Tata Consumer Products", "sector": "FMCG"},
    "TMPV": {"name": "Tata Motors", "sector": "Auto"},
    "TATASTEEL": {"name": "Tata Steel", "sector": "Metals"},
    "TECHM": {"name": "Tech Mahindra", "sector": "IT"},
    "TITAN": {"name": "Titan Company", "sector": "Consumer"},
    "ULTRACEMCO": {"name": "UltraTech Cement", "sector": "Materials"},
    "WIPRO": {"name": "Wipro", "sector": "IT"},
    "TRENT": {"name": "Trent Limited", "sector": "Retail"},
    "SHRIRAMFIN": {"name": "Shriram Finance", "sector": "Finance"}
}

# ======================================================
# PAGE CSS
# ======================================================
st.markdown("""
<style>
.block-container { padding-top:1rem; }

.page-title{
  font-size:36px;
  font-weight:900;
  background: linear-gradient(90deg, #ffffff, #525252);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

.page-subtitle{
  color:#9ca3af;
  font-size:17px;
  margin-top:10px;
}

.glass{
  background:linear-gradient(180deg,rgba(255,255,255,0.06),rgba(255,255,255,0.02));
  border:1px solid rgba(255,255,255,0.12);
  border-radius:22px;
  padding:22px;
  margin-bottom:18px;
  transition:all .35s ease;
}

.glass:hover{
  transform:translateY(-6px);
  box-shadow:0 24px 50px rgba(0,0,0,.45);
}

.stock-name{ font-size:20px; font-weight:800; }
.ticker{ font-size:13px; color:#9ca3af; }
.price{ font-size:22px; font-weight:900; }

.gain{ color:#22c55e; font-size:18px; font-weight:800; }
.loss{ color:#ef4444; font-size:18px; font-weight:800; }

.meta{ font-size:13px; color:#9ca3af; margin-top:6px; }

.badge-gain{
  background:rgba(34,197,94,.15);
  color:#22c55e;
  padding:6px 14px;
  border-radius:999px;
  font-size:12px;
  font-weight:800;
  margin-top:10px;
  display:inline-block;
}

.badge-loss{
  background:rgba(239,68,68,.15);
  color:#ef4444;
  padding:6px 14px;
  border-radius:999px;
  font-size:12px;
  font-weight:800;
  margin-top:10px;
  display:inline-block;
}

.logo{
  width:46px;
  height:46px;
  border-radius:12px;
  background:rgba(255,255,255,0.08);
  padding:6px;
}
/* =====================================================
   APEX FILTER FORM — NO BORDER, GLASS THEME
   ===================================================== */

/* Remove form border completely */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

/* Remove inner form wrapper border */
div[data-testid="stForm"] > div {
    border: none !important;
    box-shadow: none !important;
}

/* Kill BaseWeb red focus ring */
div[data-testid="stForm"]:focus-within,
div[data-baseweb="block"]:focus-within {
    outline: none !important;
    box-shadow: none !important;
}

/* Style sliders to match theme */
div[data-testid="stSlider"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 16px 14px 6px 14px;
}

/* Slider label */
div[data-testid="stSlider"] label {
    color: #e5e7eb !important;
    font-weight: 700;
}

/* Selectbox container */
div[data-testid="stSelectbox"] {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
    padding: 10px 12px;
}

/* Selectbox text */
div[data-testid="stSelectbox"] * {
    color: #e5e7eb !important;
}

/* Apply button (filter CTA) */
div[data-testid="stFormSubmitButton"] button {
    height: 46px;
    width: 100%;
    border-radius: 12px;
    background: #ffffff !important;
    color: #000000 !important;
    font-weight: 800;
    letter-spacing: .4px;
    border: none;
    transition: all .3s ease;
}

/* Apply hover */
div[data-testid="stFormSubmitButton"] button:hover {
    background: #e4e4e7 !important;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.3) !important;
    transform: translateY(-2px);
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================
st.markdown('<div class="page-title">Nifty 50 Market Movers</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">'
    'Live intraday top gaining and losing stocks strictly from the NIFTY 50 index.'
    '</div>',
    unsafe_allow_html=True
)
st.divider()
# ======================================================
# DATA FETCH (STRICT NIFTY 50 STOCKS)
# ======================================================
@st.cache_data(ttl=180, show_spinner=False)
def fetch_nifty50_movers():
    # 1. Real-time batch fetch via yfinance
    try:
        yf_symbols = [f"{sym}.NS" for sym in NIFTY_50_STOCKS.keys()]
        df = yf.download(yf_symbols, period="5d", interval="1d", progress=False)
        close = df["Close"].dropna(how="all")
        if len(close) >= 2:
            prev = close.iloc[-2]
            curr = close.iloc[-1]
            high_s = df["High"].iloc[-1]
            low_s = df["Low"].iloc[-1]
            vol_s = df["Volume"].iloc[-1]

            movers = []
            for sym, info in NIFTY_50_STOCKS.items():
                col = f"{sym}.NS"
                try:
                    c = float(curr[col])
                    p = float(prev[col])
                    if p > 0 and c > 0:
                        chg_pct = round(((c - p) / p) * 100, 2)
                        h = round(float(high_s[col]), 2)
                        l = round(float(low_s[col]), 2)
                        v = int(vol_s[col]) if not pd.isna(vol_s[col]) else 0
                        movers.append({
                            "company_name": info["name"],
                            "ticker_id": sym if sym != "TMPV" else "TATAMOTORS",
                            "exchange_type": "NSE",
                            "price": f"{c:,.2f}",
                            "raw_price": c,
                            "percent_change": chg_pct,
                            "volume": f"{v:,}" if v > 0 else "—",
                            "high": f"{h:,.2f}",
                            "low": f"{l:,.2f}",
                            "long_term_trends": "Bullish" if chg_pct > 0 else "Bearish",
                            "overall_rating": "Bullish" if chg_pct >= 1.5 else ("Bearish" if chg_pct <= -1.5 else "Neutral")
                        })
                except Exception:
                    continue

            if movers:
                g = sorted([m for m in movers if m["percent_change"] >= 0], key=lambda x: x["percent_change"], reverse=True)
                l = sorted([m for m in movers if m["percent_change"] < 0], key=lambda x: x["percent_change"])
                return {"gainers": g, "losers": l}
    except Exception:
        pass

    # 2. Resilient fallback to stock_filter_cache.json
    try:
        cache_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "stock_filter_cache.json")
        if os.path.exists(cache_path):
            with open(cache_path, "r", encoding="utf-8") as f:
                cdata = json.load(f).get("data", [])
            nifty_keys = set(NIFTY_50_STOCKS.keys()) | {"TATAMOTORS"}
            filtered = [x for x in cdata if x.get("Ticker") in nifty_keys]
            movers = []
            for x in filtered:
                chg = float(x.get("Change%", 0))
                movers.append({
                    "company_name": x.get("Name"),
                    "ticker_id": x.get("Ticker"),
                    "exchange_type": "NSE",
                    "price": f"{x.get('Price', 0):,.2f}",
                    "percent_change": chg,
                    "volume": "—",
                    "high": f"{x.get('52W_High', 0):,.2f}",
                    "low": f"{x.get('52W_Low', 0):,.2f}",
                    "long_term_trends": "Bullish" if chg >= 0 else "Bearish",
                    "overall_rating": "Bullish" if chg >= 1.0 else ("Bearish" if chg <= -1.0 else "Neutral")
                })
            g = sorted([m for m in movers if m["percent_change"] >= 0], key=lambda x: x["percent_change"], reverse=True)
            l = sorted([m for m in movers if m["percent_change"] < 0], key=lambda x: x["percent_change"])
            return {"gainers": g, "losers": l}
    except Exception:
        pass
    return {"gainers": [], "losers": []}

data = fetch_nifty50_movers()
gainers = data.get("gainers", [])
losers = data.get("losers", [])

# ======================================================
# LOGO DEV
# ======================================================
LOGO_DEV_PUBLIC_KEY = "pk_IklwgQWBS--r9KUZrBrY6g"

def get_company_logo(company):
    if not company:
        return ""
    name = company.replace(" ", "%20")
    return f"https://img.logo.dev/name/{name}?token={LOGO_DEV_PUBLIC_KEY}"

# ======================================================
# FILTERS
# ======================================================
with st.container():

    with st.form("filters"):
        c1, c2, c3 = st.columns(3)

        with c1:
            gain_limit = st.slider("▲ Minimum Gainers %", 0.0, 5.0, 0.0, 0.5)

        with c2:
            loss_limit = st.slider("▼ Maximum Losers %", -5.0, 0.0, 0.0, 0.5)

        with c3:
            show_count = st.selectbox("Show Top", [3, 5, 10], index=1)

        apply = st.form_submit_button("⌯✈ Apply Filters")

    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ======================================================
# HELPERS
# ======================================================
def pct(val):
    try:
        return float(str(val).replace("%", ""))
    except:
        return 0.0

def stock_card(stock, pct_val, gainer=True):
    move = "gain" if gainer else "loss"
    badge = "badge-gain" if gainer else "badge-loss"
    label = "GAINER" if gainer else "LOSER"

    company = stock.get("company_name", "-")
    logo = get_company_logo(company)

    st.markdown(f"""
    <div class="glass">
      <div style="display:flex;align-items:center;gap:14px;">
        <img src="{logo}" class="logo">
        <div>
          <div class="stock-name">{company}</div>
          <div class="ticker">
            {stock.get("ticker_id","-")} • {stock.get("exchange_type","")}
          </div>
        </div>
      </div>

      <br>
      <div class="price">₹ {stock.get("price","-")}</div>
      <div class="{move}">{pct_val:+.2f}%</div>

      <div class="meta">Volume: {stock.get("volume","-")}</div>
      <div class="meta">Trend: {stock.get("long_term_trends","-")}</div>
      <div class="meta">High / Low: {stock.get("high","-")} / {stock.get("low","-")}</div>
      <div class="meta">✮ Rating: {stock.get("overall_rating","-")}</div>

      <div class="{badge}">{label}</div>
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# LAYOUT
# ======================================================
left, right = st.columns(2)

with left:
    st.subheader("📈 Top Gainers")
    count = show_count
    for s in gainers:
        p = pct(s.get("percent_change"))
        if p < gain_limit or count <= 0:
            continue
        stock_card(s, p, True)
        count -= 1

with right:
    st.subheader("📉 Top Losers")
    count = show_count
    for s in losers:
        p = pct(s.get("percent_change"))
        if p > loss_limit or count <= 0:
            continue
        stock_card(s, p, False)
        count -= 1

st.divider()
st.caption("© 2025 Apex Stock Screener • Market Movers • Built with Python & Streamlit")

