import streamlit as st

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="Stock Insights · Apex",
    page_icon="icon.png",
    layout="wide"
)

import requests
import os
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
from dotenv import load_dotenv
from ui.sidebar import render_sidebar
from ui.styles import load_global_css

if not st.session_state.get("logged_in"):
    st.switch_page("合_Welcome.py")

load_global_css()
render_sidebar()

load_dotenv()
API_KEY  = os.getenv("INDIAN_API_KEY")
BASE_URL = "https://stock.indianapi.in"
HEADERS  = {"X-Api-Key": API_KEY}
LOGO_KEY = "pk_IklwgQWBS--r9KUZrBrY6g"

# ════════════════════════════════════════
#  CSS
# ════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { padding-top: 1.2rem !important; }

/* ── Page Header ── */
.si-header {
    background: linear-gradient(135deg, #111111 0%, #1a1a1a 60%, #080808 100%);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 18px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.si-header::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 65%);
    border-radius: 50%;
}
.si-header-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #ffffff;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
.si-header-tag::before {
    content: '';
    width: 5px; height: 5px;
    background: #ffffff;
    border-radius: 50%;
    animation: blink 2s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.25} }
.si-title {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #ffffff;
    margin: 0 0 0.25rem;
    letter-spacing: -0.01em;
}
.si-title span { color: #ffffff; }
.si-sub { font-size: 0.83rem; color: #8e8e93; margin: 0; }

/* ── Search ── */
div[data-testid="stTextInput"],
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] [data-baseweb="input"],
div[data-testid="stTextInput"] [data-baseweb="base-input"] {
    border: none !important; box-shadow: none !important;
    outline: none !important; background: transparent !important;
}
div[data-testid="stTextInput"] input {
    height: 48px;
    padding: 0 18px;
    border-radius: 12px !important;
    background: #111111 !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #f5f5f5 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    transition: border-color 0.2s !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #737373 !important; }
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(255,255,255,0.30) !important;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.042) !important;
}
div[data-testid="stTextInput"] input:hover { border-color: rgba(255,255,255,0.20) !important; }
div[data-testid="InputInstructions"] { display: none !important; }

div[data-testid="stFormSubmitButton"] button {
    height: 40px !important;
    width: 100% !important;
    border-radius: 12px !important;
    background: #ffffff !important;
    border: 1px solid #ffffff !important;
    color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.03em !important;
    cursor: pointer !important;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.25) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
div[data-testid="stFormSubmitButton"] button:hover {
    background: #e4e4e7 !important;
    color: #000000 !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.50) !important;
    transform: translateY(-2px) !important;
}
div[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0) !important;
}

/* ── Company Banner ── */
.co-banner {
    background: #111111;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    flex-wrap: wrap;
}
.co-logo {
    width: 52px; height: 52px;
    border-radius: 12px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.10);
    padding: 6px;
    object-fit: contain;
    flex-shrink: 0;
}
.co-name {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: #ffffff;
    margin: 0 0 3px;
    letter-spacing: -0.01em;
}
.co-industry {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #737373;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.co-price-block { margin-left: auto; text-align: right; }
.co-price {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #ffffff;
    margin: 0;
}
.co-price-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #737373;
    margin-top: 3px;
}

/* ── Metric Cards ── */
.metric-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 0.8rem;
    margin-bottom: 1.2rem;
}
.metric-card {
    background: #111111;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: rgba(255,255,255,0.12); }
.metric-card-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #737373;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 5px;
}
.metric-card-value {
    font-size: 1.05rem;
    font-weight: 600;
    color: #f5f5f5;
    font-family: 'DM Sans', sans-serif;
}
.metric-card-delta {
    font-size: 0.75rem;
    margin-top: 3px;
    font-family: 'JetBrains Mono', monospace;
}
.delta-pos { color: #22c55e; }
.delta-neg { color: #ef4444; }

/* ── Section Header ── */
.sec-hdr {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 1.4rem 0 0.8rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.sec-hdr-icon {
    width: 28px; height: 28px;
    border-radius: 7px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
}
.sec-hdr-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: #cce9ff;
    margin: 0;
}
.sec-hdr-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    color: #737373;
    margin-left: auto;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Chart Toggle ── */
div[data-testid="stCheckbox"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    color: #8e8e93 !important;
    letter-spacing: 0.06em !important;
}

/* ── Streamlit Metric override ── */
[data-testid="stMetric"] {
    background: #111111 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stMetric"]:hover { border-color: rgba(255,255,255,0.12) !important; }
[data-testid="stMetricLabel"] { font-size: 10px !important; color: #737373 !important; font-family: 'JetBrains Mono', monospace !important; text-transform: uppercase !important; letter-spacing: 0.08em !important; }
[data-testid="stMetricValue"] { font-size: 17px !important; font-weight: 600 !important; color: #f5f5f5 !important; }
[data-testid="stMetricDelta"] { font-size: 11px !important; }
div[data-testid="stForm"] { border: none !important; padding: 0 !important; background: transparent !important; }
div[data-testid="column"] { padding-top: 0 !important; }

/* ── Description ── */
.desc-card {
    background: #111111;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    font-size: 0.9rem;
    line-height: 1.85;
    color: #7aa7c7;
    margin-bottom: 1.2rem;
}

/* ── News Cards ── */
.news-card {
    display: flex;
    gap: 16px;
    background: #111111;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 12px;
    transition: all 0.25s ease;
    text-decoration: none;
}
.news-card:hover {
    border-color: rgba(255, 255, 255, 0.168);
    transform: translateY(-2px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.3);
}
.news-img {
    width: 130px; height: 85px;
    border-radius: 10px;
    object-fit: cover;
    flex-shrink: 0;
    background: rgba(255,255,255,0.04);
}
.news-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: #cce9ff;
    margin-bottom: 5px;
    line-height: 1.4;
}
.news-summary {
    font-size: 0.8rem;
    color: #8e8e93;
    line-height: 1.55;
    margin-bottom: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.news-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #737373;
    display: flex;
    gap: 12px;
    letter-spacing: 0.05em;
}
.news-link {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #ffffff;
    text-decoration: none;
    margin-top: 6px;
    display: inline-block;
    letter-spacing: 0.05em;
}

/* ── Shareholding ── */
.sh-title {
    font-family: 'DM Serif Display', serif;
    font-size: 0.95rem;
    color: #cce9ff;
    margin: 1rem 0 0.6rem;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden !important; }

/* ── Empty state ── */
.empty-search {
    text-align: center;
    padding: 4rem 2rem;
}
.empty-mono {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #1e3a52;
    letter-spacing: 0.18em;
    margin-bottom: 1rem;
}
.empty-title { font-size: 1rem; color: #737373; font-weight: 600; margin-bottom: 0.3rem; }
.suggestion-chips { display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-top:1rem; }
.s-chip { font-family:'JetBrains Mono',monospace;font-size:0.7rem;padding:5px 13px;border-radius:20px;border:1px solid rgba(255,255,255,0.10);color:#ffffff;background:rgba(255, 255, 255, 0.030);letter-spacing:0.08em; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════
st.markdown("""
<div class="si-header">
    <div class="si-header-tag">Live Market Data · IndianAPI.in</div>
    <p class="si-title">Stock <span>Insights</span></p>
    <p class="si-sub">Deep company analysis · Valuation · Shareholding · News</p>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
#  SEARCH
# ════════════════════════════════════════
with st.form("stock_form", clear_on_submit=False):
    c1, c2 = st.columns([7, 1])
    with c1:
        stock_name = st.text_input(
            "",
            placeholder="Search any stock by name  e.g. Reliance, TCS, HDFC Bank...",
            label_visibility="collapsed"
        )
    with c2:
        search = st.form_submit_button("Search →")

# ════════════════════════════════════════
#  HELPERS
# ════════════════════════════════════════
def get_logo(company_name):
    name = company_name.replace(" ", "%20")
    return f"https://img.logo.dev/name/{name}?token={LOGO_KEY}"

def to_cr(value, divisor=1):
    try:
        return f"₹{float(value)/divisor:,.2f} Cr"
    except Exception:
        return "-"

def get_val(section, *keywords):
    if not isinstance(section, list):
        return "-"
    for item in section:
        key = str(item.get("key","")).lower()
        for kw in keywords:
            if kw.lower() in key:
                v = item.get("value")
                return "-" if v in [None,"","NULL"] else v
    return "-"

def parse_ds(values, col):
    if not values:
        return None
    df = pd.DataFrame(values)
    if df.shape[1] < 2:
        return None
    df = df.iloc[:,:2]
    df.columns = ["date", col]
    return df

def delta_color(val):
    try:
        return "delta-pos" if float(str(val).replace("%","")) >= 0 else "delta-neg"
    except Exception:
        return ""

def sec(icon, title, sub=""):
    sub_html = f'<span class="sec-hdr-sub">{sub}</span>' if sub else ""
    st.markdown(
        f'<div class="sec-hdr">'
        f'<div class="sec-hdr-icon">{icon}</div>'
        f'<p class="sec-hdr-title">{title}</p>'
        f'{sub_html}</div>',
        unsafe_allow_html=True
    )

@st.cache_data(ttl=300, show_spinner=False)
def fetch_stock(name):
    r = requests.get(f"{BASE_URL}/stock", headers=HEADERS, params={"name": name}, timeout=15)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=300, show_spinner=False)
def fetch_hist(name):
    r = requests.get(f"{BASE_URL}/historical_data", headers=HEADERS,
                     params={"stock_name": name, "period": "1yr", "filter": "price"}, timeout=10)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=300, show_spinner=False)
def fetch_yfinance_ohlc(stock_name, period="1y"):
    clean = str(stock_name).strip().upper()
    MAPPINGS = {
        "INFOSYS": "INFY",
        "HDFC BANK": "HDFCBANK",
        "ICICI BANK": "ICICIBANK",
        "KOTAK BANK": "KOTAKBANK",
        "KOTAK MAHINDRA BANK": "KOTAKBANK",
        "STATE BANK OF INDIA": "SBIN",
        "SBI": "SBIN",
        "TATA MOTORS": "TMPV",
        "TATAMOTORS": "TMPV",
        "TATA CONSULTANCY SERVICES": "TCS",
        "RELIANCE INDUSTRIES": "RELIANCE",
        "BHARTI AIRTEL": "BHARTIARTL",
        "AIRTEL": "BHARTIARTL",
        "LARSEN & TOUBRO": "LT",
        "L&T": "LT",
        "BAJAJ FINANCE": "BAJFINANCE",
        "HINDUSTAN UNILEVER": "HINDUNILVR",
        "HUL": "HINDUNILVR",
        "ITC": "ITC",
        "ASIAN PAINTS": "ASIANPAINT",
        "MARUTI SUZUKI": "MARUTI",
        "MARUTI": "MARUTI",
        "SUN PHARMA": "SUNPHARMA",
        "TITAN": "TITAN",
        "ADANI ENTERPRISES": "ADANIENT",
        "ADANI PORTS": "ADANIPORTS",
        "ULTRATECH CEMENT": "ULTRACEMCO",
        "NESTLE": "NESTLEIND",
        "POWER GRID": "POWERGRID",
        "NTPC": "NTPC",
        "AXIS BANK": "AXISBANK",
        "MAHINDRA & MAHINDRA": "M&M",
        "M&M": "M&M",
        "TATA STEEL": "TATASTEEL",
        "COAL INDIA": "COALINDIA",
        "ONGC": "ONGC",
        "HCL TECH": "HCLTECH",
        "HCL": "HCLTECH",
        "WIPRO": "WIPRO",
        "BAJAJ FINSERV": "BAJAJFINSV",
        "JSW STEEL": "JSWSTEEL",
        "TECH MAHINDRA": "TECHM",
        "GRASIM": "GRASIM",
        "INDUSIND BANK": "INDUSINDBK",
        "HINDALCO": "HINDALCO",
        "CIPLA": "CIPLA",
        "DIVIS LAB": "DIVISLAB",
        "DR REDDY": "DRREDDY",
        "EICHER MOTORS": "EICHERMOT",
        "APOLLO HOSPITALS": "APOLLOHOSP",
        "HERO MOTOCORP": "HEROMOTOCO",
        "BPCL": "BPCL",
        "BRITANNIA": "BRITANNIA",
    }
    sym_cand = MAPPINGS.get(clean, clean.replace(" ", ""))
    for suffix in [".NS", ".BO", ""]:
        try:
            t = yf.Ticker(f"{sym_cand}{suffix}" if suffix else sym_cand)
            h = t.history(period=period)
            if not h.empty and len(h) > 5:
                h = h.reset_index()
                h["Date"] = pd.to_datetime(h["Date"]).dt.tz_localize(None)
                return h
        except Exception:
            pass
    try:
        s = yf.Search(stock_name, max_results=3)
        for quote in s.quotes:
            sym = quote.get("symbol", "")
            if sym.endswith(".NS") or sym.endswith(".BO"):
                t = yf.Ticker(sym)
                h = t.history(period=period)
                if not h.empty and len(h) > 5:
                    h = h.reset_index()
                    h["Date"] = pd.to_datetime(h["Date"]).dt.tz_localize(None)
                    return h
    except Exception:
        pass
    return None

# ════════════════════════════════════════
#  STATE
# ════════════════════════════════════════
if search and stock_name:
    st.session_state["si_stock"] = stock_name

# ════════════════════════════════════════
#  EMPTY STATE
# ════════════════════════════════════════
if "si_stock" not in st.session_state:
    st.markdown("""
    <div class="empty-search">
        <div class="empty-mono">[ APEX · STOCK INSIGHTS · LIVE DATA ]</div>
        <div class="empty-title">Search a stock to begin</div>
        <p style="color:#1e3a52;font-size:0.82rem;margin:0">Fundamentals · Charts · Shareholding · News</p>
        <div class="suggestion-chips">
            <span class="s-chip">RELIANCE</span>
            <span class="s-chip">TCS</span>
            <span class="s-chip">HDFC BANK</span>
            <span class="s-chip">INFOSYS</span>
            <span class="s-chip">WIPRO</span>
            <span class="s-chip">ZOMATO</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ════════════════════════════════════════
#  FETCH
# ════════════════════════════════════════
stock_name = st.session_state["si_stock"]

with st.spinner(f"Fetching {stock_name} data..."):
    try:
        data  = fetch_stock(stock_name)
        chart = fetch_hist(stock_name)
    except requests.exceptions.Timeout:
        st.error("⏱ API timeout. Please try again.")
        st.stop()
    except requests.exceptions.HTTPError as e:
        st.error(f"API error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error: {e}")
        st.stop()

# ════════════════════════════════════════
#  COMPANY BANNER
# ════════════════════════════════════════
company_name  = data.get("companyName", "-")
industry      = data.get("industry", "-")
price         = data.get("currentPrice", {})
nse_price     = price.get("NSE", "-")
bse_price     = price.get("BSE", "-")
pct_change    = data.get("percentChange", 0)
year_high     = data.get("yearHigh", "-")
year_low      = data.get("yearLow", "-")
logo_url      = get_logo(company_name)

try:
    pct_float  = float(pct_change)
    pct_color  = "#22c55e" if pct_float >= 0 else "#ef4444"
    pct_sign   = "▲" if pct_float >= 0 else "▼"
    pct_display= f'{pct_sign} {abs(pct_float):.2f}%'
except Exception:
    pct_color   = "#8e8e93"
    pct_display = str(pct_change)

st.markdown(f"""
<div class="co-banner">
    <img src="{logo_url}" class="co-logo" onerror="this.style.display='none'">
    <div>
        <p class="co-name">{company_name}</p>
        <p class="co-industry">{industry}</p>
    </div>
    <div class="co-price-block">
        <p class="co-price">₹{nse_price}</p>
        <p class="co-price-sub" style="color:{pct_color}">{pct_display} TODAY &nbsp;·&nbsp; NSE</p>
        <p class="co-price-sub">BSE ₹{bse_price} &nbsp;·&nbsp; 52W ₹{year_low} – ₹{year_high}</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
#  PRICE CHART (CANDLESTICK + LINE + DMA + VOLUME)
# ════════════════════════════════════════
sec("📈", "Price Chart", "1 YEAR · DAILY")

# 1. Fetch OHLC data via Yahoo Finance (with IndianAPI fallback)
ohlc_df = fetch_yfinance_ohlc(stock_name, period="1y")

datasets   = chart.get("datasets", [])
price_df   = None
dma50_df   = None
dma200_df  = None
volume_df  = None

for ds in datasets:
    metric = ds.get("metric","").lower()
    values = ds.get("values",[])
    if   metric == "price":   price_df  = parse_ds(values, "price")
    elif metric == "dma50":   dma50_df  = parse_ds(values, "dma50")
    elif metric == "dma200":  dma200_df = parse_ds(values, "dma200")
    elif metric == "volume":  volume_df = parse_ds(values, "volume")

if (ohlc_df is None or ohlc_df.empty) and (price_df is None or price_df.empty):
    st.warning("No price data available.")
else:
    # Controls row
    tc1, tc2, tc3, tc4 = st.columns([1.1, 1.1, 1.1, 1.7])
    with tc1: show_50  = st.checkbox("50 DMA", value=True)
    with tc2: show_200 = st.checkbox("200 DMA", value=True)
    with tc3: show_vol = st.checkbox("Volume", value=False)
    with tc4:
        # Default to Candlestick when OHLC is available
        chart_options = ["🕯 Candlestick", "📈 Line"] if (ohlc_df is not None and not ohlc_df.empty) else ["📈 Line"]
        chart_type = st.radio("Chart Type", chart_options, horizontal=True, label_visibility="collapsed")

    fig = go.Figure()

    if chart_type == "🕯 Candlestick" and ohlc_df is not None and not ohlc_df.empty:
        # Compute DMAs from OHLC Close if needed
        ohlc_df["dma50"]  = ohlc_df["Close"].rolling(50, min_periods=1).mean()
        ohlc_df["dma200"] = ohlc_df["Close"].rolling(200, min_periods=1).mean()

        fig.add_trace(go.Candlestick(
            x=ohlc_df["Date"],
            open=ohlc_df["Open"],
            high=ohlc_df["High"],
            low=ohlc_df["Low"],
            close=ohlc_df["Close"],
            name="OHLC",
            increasing_line_color="#22c55e",
            increasing_fillcolor="rgba(34, 197, 94, 0.75)",
            decreasing_line_color="#ef4444",
            decreasing_fillcolor="rgba(239, 68, 68, 0.75)"
        ))

        if show_50:
            fig.add_trace(go.Scatter(
                x=ohlc_df["Date"], y=ohlc_df["dma50"],
                name="50 DMA", mode="lines",
                line=dict(color="#22c55e", width=1.5, dash="dot"),
                hovertemplate="50 DMA: ₹%{y:,.2f}<extra></extra>"
            ))
        if show_200:
            fig.add_trace(go.Scatter(
                x=ohlc_df["Date"], y=ohlc_df["dma200"],
                name="200 DMA", mode="lines",
                line=dict(color="#f59e0b", width=1.5, dash="dot"),
                hovertemplate="200 DMA: ₹%{y:,.2f}<extra></extra>"
            ))
        if show_vol and "Volume" in ohlc_df.columns:
            vol_colors = [
                "rgba(34, 197, 94, 0.35)" if c >= o else "rgba(239, 68, 68, 0.35)"
                for c, o in zip(ohlc_df["Close"], ohlc_df["Open"])
            ]
            fig.add_trace(go.Bar(
                x=ohlc_df["Date"], y=ohlc_df["Volume"],
                name="Volume", yaxis="y2",
                marker_color=vol_colors,
                hovertemplate="Vol: %{y:,.0f}<extra></extra>"
            ))

    else:
        # Line Chart mode (using OHLC Close if available, or IndianAPI price_df)
        if ohlc_df is not None and not ohlc_df.empty:
            df_plot = ohlc_df.copy()
            df_plot["price"] = df_plot["Close"]
            df_plot["date"] = df_plot["Date"]
            df_plot["dma50"]  = df_plot["Close"].rolling(50, min_periods=1).mean()
            df_plot["dma200"] = df_plot["Close"].rolling(200, min_periods=1).mean()
            df_plot["volume"] = df_plot["Volume"]
        else:
            price_df["date"]  = pd.to_datetime(price_df["date"], errors="coerce")
            price_df["price"] = pd.to_numeric(price_df["price"], errors="coerce")
            price_df = price_df.dropna()
            for df_, col_ in [(dma50_df,"dma50"),(dma200_df,"dma200"),(volume_df,"volume")]:
                if df_ is not None:
                    df_["date"] = pd.to_datetime(df_["date"], errors="coerce")
                    df_[col_]   = pd.to_numeric(df_[col_], errors="coerce")
                    price_df    = price_df.merge(df_, on="date", how="left")
            df_plot = price_df.sort_values("date")

        fig.add_trace(go.Scatter(
            x=df_plot["date"], y=df_plot["price"],
            name="Price", mode="lines",
            line=dict(color="#ffffff", width=2.2),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>₹%{y:,.2f}<extra></extra>"
        ))
        if show_50 and "dma50" in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot["date"], y=df_plot["dma50"],
                name="50 DMA", mode="lines",
                line=dict(color="#22c55e", width=1.6, dash="dot")
            ))
        if show_200 and "dma200" in df_plot.columns:
            fig.add_trace(go.Scatter(
                x=df_plot["date"], y=df_plot["dma200"],
                name="200 DMA", mode="lines",
                line=dict(color="#f59e0b", width=1.6, dash="dot")
            ))
        if show_vol and "volume" in df_plot.columns:
            fig.add_trace(go.Bar(
                x=df_plot["date"], y=df_plot["volume"],
                name="Volume", yaxis="y2",
                marker_color="rgba(255,255,255,0.12)"
            ))

    fig.update_layout(
        height=440,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a1a1aa", size=11, family="JetBrains Mono"),
        xaxis=dict(
            showgrid=True,
            gridcolor="rgba(255,255,255,0.04)",
            zeroline=False,
            rangeslider=dict(visible=False)
        ),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False, title="Price (₹)"),
        yaxis2=dict(title="Volume", overlaying="y", side="right", showgrid=False, showticklabels=False),
        legend=dict(orientation="h", y=1.03, x=0, font=dict(size=11, family="JetBrains Mono")),
        margin=dict(l=8, r=8, t=10, b=8),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)
# ════════════════════════════════════════
#  KEY METRICS
# ════════════════════════════════════════
ratio      = data.get("keyMetrics") or {}
valuation  = ratio.get("valuation", [])
financial  = ratio.get("financialstrength", [])
management = ratio.get("mgmtEffectiveness", [])
pav        = ratio.get("priceandVolume", [])
inc_stmt   = ratio.get("incomeStatement", [])
margins    = ratio.get("margins", [])
growth     = ratio.get("growth", [])

pe   = get_val(valuation,  "pPerE")
pb   = get_val(valuation,  "priceToBook")
mc   = get_val(pav,        "marketCap")
dv   = get_val(valuation,  "currentDividendYield")
de   = get_val(financial,  "totalDebtPerT")
cr   = get_val(financial,  "currentRatioMost")
roi  = get_val(management, "returnOnInvestment")
om   = get_val(margins,    "operatingMarginTrailing")
cf   = get_val(financial,  "freeCashFlowMostRecent")
gw   = get_val(growth,     "revenueGrowthRate5")
rv   = get_val(inc_stmt,   "revenueTrailing")
ni   = get_val(inc_stmt,   "netIncomeAvailableToCommonTrailing12")
ebt  = get_val(inc_stmt,   "earningsBeforeTaxesTrailing12")
rvf  = get_val(inc_stmt,   "revenueMostRecent")
nif  = get_val(inc_stmt,   "netIncomeAvailabletoCommonNormalize")
ebtf = get_val(inc_stmt,   "eBITDMostRecentFiscal")
dt   = get_val(valuation,  "netDebtLFY")
tv10 = get_val(pav,        "avgTradingVolumeLast10")
tv3m = get_val(pav,        "avgTradingVolumeLast3")

sec("💹", "Valuation & Ratios", "KEY METRICS")
c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("P/E Ratio",      pe)
c2.metric("P/B Ratio",      pb)
c3.metric("Current Ratio",  cr)
c4.metric("ROI",            f"{roi}%" if roi!="-" else "-")
c5.metric("Debt/Equity",    de)

c6,c7,c8 = st.columns(3)
c6.metric("Market Cap",     to_cr(mc))
c7.metric("Operating Margin",f"{om}%" if om!="-" else "-")
c8.metric("Free Cash Flow", to_cr(cf))

sec("📊", "Income Statement", "TRAILING 12 MONTHS & LFY")
i1,i2,i3 = st.columns(3)
i1.metric("Revenue (TTM)",   to_cr(rv, 10))
i2.metric("Net Income (TTM)",to_cr(ni, 10))
i3.metric("EBT (TTM)",       to_cr(ebt, 10))

j1,j2,j3 = st.columns(3)
j1.metric("Revenue (LFY)",   to_cr(rvf, 10))
j2.metric("Net Income (LFY)",to_cr(nif, 10))
j3.metric("EBITDA (LFY)",    to_cr(ebtf, 10))

v1,v2,v3,v4,v5 = st.columns(5)
v1.metric("Net Debt (LFY)",  f"{dt} Cr" if dt!="-" else "-")
v2.metric("Dividend Yield",  f"{dv}%"   if dv!="-" else "-")
v3.metric("Revenue Growth 5Y",f"{gw}%"  if gw!="-" else "-")
v4.metric("Avg Vol 10D",     f"{tv10}M" if tv10!="-" else "-")
v5.metric("Avg Vol 3M",      f"{tv3m}M" if tv3m!="-" else "-")

# ════════════════════════════════════════
#  SHAREHOLDING
# ════════════════════════════════════════
shareholding = data.get("shareholding", [])
if shareholding:
    sec("🏦", "Shareholding Pattern", "HISTORICAL TREND")
    for item in shareholding:
        title = item.get("displayName", "—")
        rows  = []
        for row in item.get("categories", []):
            date = row.get("holdingDate")
            pct  = row.get("percentage")
            if date is None: continue
            try: pct = round(float(pct), 2)
            except: pct = None
            rows.append({"Date": date, "Holding %": pct})

        if not rows: continue
        df = pd.DataFrame(rows)
        df["Date"] = pd.to_datetime(df["Date"])

        st.markdown(f'<p class="sh-title">{title}</p>', unsafe_allow_html=True)

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df["Date"], y=df["Holding %"],
            mode="lines+markers", name="Holding %",
            line=dict(color="#ffffff", width=2),
            marker=dict(size=5, color="#ffffff"),
            hovertemplate="<b>%{x|%d %b %Y}</b><br>%{y:.2f}%<extra></extra>"
        ))
        fig2.update_layout(
            height=260,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#7aa7c7", size=10, family="JetBrains Mono"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.04)", zeroline=False, title="Holding (%)"),
            margin=dict(l=8,r=8,t=8,b=8), hovermode="x unified",
            showlegend=False
        )
        col1, col2 = st.columns([3, 1])
        with col1:
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar":False})
        with col2:
            df_sorted = df.sort_values("Date", ascending=False).reset_index(drop=True)
            table_rows_html = ""
            for _, r in df_sorted.iterrows():
                dt_val = r["Date"].strftime("%d %b %Y") if pd.notnull(r["Date"]) else "—"
                pct_val = float(r["Holding %"]) if pd.notnull(r["Holding %"]) else 0.0
                bar_w = min(100.0, max(0.0, pct_val))
                table_rows_html += (
                    f'<div style="display:flex;align-items:center;justify-content:space-between;padding:10px 14px;border-bottom:1px solid rgba(255,255,255,0.05);">'
                    f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:12px;color:#f4f4f5;font-weight:500;">{dt_val}</span>'
                    f'<div style="display:flex;align-items:center;gap:10px;">'
                    f'<div style="width:44px;height:4px;background:rgba(255,255,255,0.08);border-radius:2px;overflow:hidden;">'
                    f'<div style="width:{bar_w}%;height:100%;background:#ffffff;border-radius:2px;"></div>'
                    f'</div>'
                    f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:12.5px;font-weight:700;color:#ffffff;min-width:48px;text-align:right;">{pct_val:.2f}%</span>'
                    f'</div>'
                    f'</div>'
                )

            sh_card = (
                f'<div style="background:linear-gradient(180deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.015) 100%);'
                f'border:1px solid rgba(255,255,255,0.10);border-radius:14px;height:260px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 8px 24px rgba(0,0,0,0.45);">'
                f'<div style="display:flex;align-items:center;justify-content:space-between;padding:11px 14px;background:rgba(255,255,255,0.03);border-bottom:1px solid rgba(255,255,255,0.08);font-family:\'JetBrains Mono\',monospace;font-size:10px;font-weight:700;color:#a1a1aa;letter-spacing:0.08em;text-transform:uppercase;">'
                f'<span>QUARTER</span>'
                f'<span>HOLDING</span>'
                f'</div>'
                f'<div style="flex:1;overflow-y:auto;">'
                f'{table_rows_html}'
                f'</div>'
                f'</div>'
            )
            st.markdown(sh_card, unsafe_allow_html=True)

# ════════════════════════════════════════
#  COMPANY DESCRIPTION
# ════════════════════════════════════════
description = data.get("companyProfile", {}).get("companyDescription")
if description:
    sec("🏢", "Company Description")
    st.markdown(f'<div class="desc-card">{description}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════
#  NEWS
# ════════════════════════════════════════
news = data.get("recentNews", [])
if news:
    sec("📰", "Recent News", f"TOP {min(len(news),8)} ARTICLES")
    for item in news[:8]:
        headline = item.get("headline", "-")
        summary  = item.get("summary", "-")
        read_t   = item.get("timeToRead", "-")
        date_str = item.get("date", "")[:10]
        image    = (item.get("leadMedia",{}).get("image",{})
                       .get("images",{}).get("thumbnailImage",""))
        url      = "https://www.livemint.com" + item.get("metadata",{}).get("url","")

        st.markdown(f"""
        <div class="news-card">
            <img src="{image}" class="news-img"
                 onerror="this.style.background='rgba(255,255,255,0.04)';this.src=''">
            <div style="flex:1;min-width:0">
                <div class="news-title">{headline}</div>
                <div class="news-summary">{summary}</div>
                <div class="news-meta">
                    <span>⏱ {read_t} min read</span>
                    <span>📅 {date_str}</span>
                </div>
                <a href="{url}" target="_blank" class="news-link">READ FULL ARTICLE →</a>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════
st.markdown(
    '<p style="text-align:center;font-family:JetBrains Mono,monospace;font-size:0.65rem;'
    'color:#0f2333;margin-top:2rem;letter-spacing:0.1em">'
    '© 2026 APEX STOCK SCREENER · STOCK INSIGHTS · INDIANAPI.IN</p>',
    unsafe_allow_html=True
)