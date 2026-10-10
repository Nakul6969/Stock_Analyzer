import streamlit as st
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import os
import json

st.set_page_config(
    page_title="Apex Stock Screener | Filter",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("Please log in to access this page.")
    st.stop()

from ui.sidebar import render_sidebar
from ui.styles import load_global_css
load_global_css()
render_sidebar()

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');

:root {
  --bg1:#000000; --bg2:#0c0c0c; --bg3:#000000;
  --glass:rgba(255,255,255,0.06);
  --border:rgba(255,255,255,0.12);
  --accent:#ffffff; --accent2:#e4e4e7; --accent3:#a3a3a3;
  --danger:#f87171; --warn:#fbbf24;
  --text:#e5e7eb; --muted:#9ca3af;
}

.stApp {
  background:
    radial-gradient(1200px 600px at 15% 10%, rgba(255,255,255,0.035), transparent),
    radial-gradient(1000px 500px at 85% 20%, rgba(255,255,255,0.025), transparent),
    linear-gradient(180deg, var(--bg1) 0%, var(--bg2) 55%, var(--bg3) 100%);
  color: var(--text);
  font-family: 'Sora', Inter, system-ui, sans-serif;
  min-height: 100vh;
  animation: fadeIn 0.6s ease;
}
@keyframes fadeIn { from{opacity:0} to{opacity:1} }
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"] { background: transparent !important; }
.block-container { padding-top: 1rem !important; }

.hero-title {
  font-size: 36px; font-weight: 900;
  background: linear-gradient(90deg, #ffffff, #a3a3a3);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.hero-subtitle { font-size: 15px; color: var(--muted); margin-top: 6px; }

/* ── FILTER PANEL ── */
.filter-panel {
  background: linear-gradient(180deg, var(--glass), rgba(255,255,255,0.02));
  border: 1px solid var(--border);
  border-radius: 22px; padding: 24px 28px 20px;
  position: relative; overflow: hidden; margin-bottom: 22px;
}
.filter-panel::before {
  content:''; position:absolute; top:0;left:0;right:0; height:2px;
  background: linear-gradient(90deg,#ffffff,#a3a3a3,transparent);
}
.section-label {
  font-size:11px; font-weight:700; letter-spacing:0.13em;
  text-transform:uppercase; color:var(--accent2); margin-bottom:16px;
}
.filter-group-label {
  font-size:12px; color:var(--muted); font-weight:600;
  margin-bottom:5px; display:block;
}

/* ── NUMBER INPUT OVERRIDES ── */
input[type=number] {
  background: rgba(255,255,255,0.05) !important;
  border: 1px solid rgba(255,255,255,0.15) !important;
  border-radius: 10px !important;
  color: #e2e8f0 !important;
  font-family: 'JetBrains Mono', monospace !important;
}
input[type=number]:focus {
  border-color: rgba(255, 255, 255, 0.300) !important;
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.060) !important;
}
.stNumberInput label { color: var(--muted) !important; font-size: 12px !important; }
div[data-testid="stNumberInput"] { margin-bottom: 0 !important; }

/* ── PRESET CHIPS ── */
.preset-label {
  font-size:11px; font-weight:700; letter-spacing:0.1em;
  text-transform:uppercase; color:var(--muted); margin-bottom:8px;
}
.chips-row { display:flex; flex-wrap:wrap; gap:8px; }
.chip {
  display:inline-block; padding:5px 14px; border-radius:20px;
  font-size:12px; font-weight:600; cursor:pointer;
  border:1px solid rgba(255,255,255,0.15);
  background:rgba(255,255,255,0.04); color:var(--muted);
  transition:all 0.2s ease;
}
.chip:hover { border-color:rgba(255, 255, 255, 0.240); color:var(--accent2); }
.chip.active {
  background:rgba(255,255,255,0.08); color:var(--accent2);
  border-color:rgba(255, 255, 255, 0.240);
}
.chip.active-green {
  background:rgba(34,197,94,0.12); color:var(--accent);
  border-color:rgba(34,197,94,0.35);
}

/* ── DIVIDER ── */
.mini-divider { height:1px; background:rgba(255,255,255,0.08); margin:18px 0; }

/* ── SECTOR CHIPS (same style, different state) ── */
.sector-chip {
  display:inline-block; padding:4px 12px; border-radius:20px;
  font-size:12px; cursor:pointer;
  border:1px solid rgba(255,255,255,0.12);
  background:rgba(255,255,255,0.03); color:var(--muted);
  transition:all 0.2s;
}
.sector-chip:hover { border-color:rgba(129,140,248,0.4); color:var(--accent3); }

/* ── RESULT CARDS ── */
.count-badge {
  display:inline-block; background:rgba(255,255,255,0.08);
  color:var(--accent2); border:1px solid rgba(255,255,255,0.15);
  border-radius:10px; padding:2px 12px; font-size:13px; font-weight:700; margin-left:10px;
}
.stock-card {
  background: linear-gradient(160deg, rgba(255,255,255,0.065), rgba(255,255,255,0.02));
  border:1px solid var(--border); border-radius:18px; padding:18px 22px; margin-bottom:12px;
  position:relative; overflow:hidden;
  transition:border-color 0.3s, box-shadow 0.3s, transform 0.3s;
}
.stock-card::before {
  content:''; position:absolute; top:0;left:0;right:0; height:2px;
  background:linear-gradient(90deg,#ffffff,#a3a3a3,transparent); opacity:0; transition:opacity 0.3s;
}
.stock-card:hover::before { opacity:1; }
.stock-card:hover { transform:translateY(-3px); border-color:rgba(255, 255, 255, 0.168); box-shadow:0 20px 45px rgba(0,0,0,0.5); }
.s-name  { font-size:15px; font-weight:800; color:#f1f5f9; }
.s-sym   { font-size:11px; color:var(--accent2); background:rgba(255, 255, 255, 0.060); border:1px solid rgba(255, 255, 255, 0.120); padding:2px 8px; border-radius:6px; display:inline-block; margin-left:6px; font-family:'JetBrains Mono',monospace; }
.s-price { font-size:24px; font-weight:900; color:#f8fafc; font-family:'JetBrains Mono',monospace; }
.chg-pos { color:var(--accent); font-size:13px; font-weight:700; }
.chg-neg { color:var(--danger); font-size:13px; font-weight:700; }
.stat-row { display:flex; flex-wrap:wrap; gap:8px; margin-top:12px; }
.stat-badge { background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08); border-radius:10px; padding:5px 12px; font-size:12px; color:var(--muted); }
.stat-badge b { color:#e2e8f0; font-family:'JetBrains Mono',monospace; }
.wk-track { height:4px; border-radius:2px; background:rgba(255,255,255,0.07); margin:6px 0 2px; }
.empty-state { text-align:center; padding:60px 20px; color:var(--muted); font-size:15px; }

/* ── TABLE ── */
div[data-testid="stDataFrame"] > div {
  background:#000000 !important; border-radius:14px !important;
  border:1px solid rgba(255,255,255,0.1) !important; overflow:hidden;
}
div[data-testid="stDataFrame"] iframe { background:#000000 !important; color-scheme:dark; }
.stSelectbox>label { color:var(--muted) !important; font-size:12px !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STOCK UNIVERSE (NIFTY 100)
# ─────────────────────────────────────────────
STOCKS = {
    "ADANIENT":"Energy",       "ADANIPORTS":"Infrastructure", "APOLLOHOSP":"Healthcare",
    "ASIANPAINT":"FMCG",       "AXISBANK":"Banking",          "BAJAJ-AUTO":"Auto",
    "BAJFINANCE":"Finance",    "BAJAJFINSV":"Finance",        "BEL":"Defence",
    "BHARTIARTL":"Telecom",    "BPCL":"Energy",               "BRITANNIA":"FMCG",
    "CIPLA":"Pharma",          "COALINDIA":"Energy",          "DRREDDY":"Pharma",
    "EICHERMOT":"Auto",        "GRASIM":"Materials",          "HCLTECH":"IT",
    "HDFCBANK":"Banking",      "HDFCLIFE":"Insurance",        "HEROMOTOCO":"Auto",
    "HINDALCO":"Metals",       "HINDUNILVR":"FMCG",           "ICICIBANK":"Banking",
    "ITC":"FMCG",              "INDUSINDBK":"Banking",        "INFY":"IT",
    "JSWSTEEL":"Metals",       "KOTAKBANK":"Banking",         "LT":"Infrastructure",
    "M&M":"Auto",              "MARUTI":"Auto",               "NESTLEIND":"FMCG",
    "NTPC":"Energy",           "ONGC":"Energy",               "POWERGRID":"Energy",
    "RELIANCE":"Energy",       "SBILIFE":"Insurance",         "SBIN":"Banking",
    "SUNPHARMA":"Pharma",      "TCS":"IT",                    "TATACONSUM":"FMCG",
    "TATAMOTORS":"Auto",       "TATASTEEL":"Metals",          "TECHM":"IT",
    "TITAN":"Consumer",        "ULTRACEMCO":"Materials",      "UPL":"Chemicals",
    "WIPRO":"IT",              "ABB":"Capital Goods",         "ADANIGREEN":"Energy",
    "AMBUJACEM":"Materials",   "AUROPHARMA":"Pharma",         "BALKRISIND":"Auto",
    "BANDHANBNK":"Banking",    "BERGEPAINT":"FMCG",           "BIOCON":"Pharma",
    "BOSCHLTD":"Auto",         "CANBK":"Banking",             "CHOLAFIN":"Finance",
    "COLPAL":"FMCG",           "CONCOR":"Infrastructure",     "DABUR":"FMCG",
    "DLF":"Real Estate",       "DIVISLAB":"Pharma",           "DMART":"Retail",
    "GAIL":"Energy",           "GODREJCP":"FMCG",             "HAVELLS":"Capital Goods",
    "ICICIGI":"Insurance",     "ICICIPRU":"Insurance",        "IDFCFIRSTB":"Banking",
    "INDHOTEL":"Consumer",     "INDUSTOWER":"Telecom",        "IOC":"Energy",
    "IRCTC":"Consumer",        "JUBLFOOD":"Consumer",         "LICHSGFIN":"Finance",
    "LUPIN":"Pharma",          "MARICO":"FMCG",               "MFSL":"Insurance",
    "MOTHERSON":"Auto",        "MPHASIS":"IT",                "MRF":"Auto",
    "NAUKRI":"IT",             "OFSS":"IT",                   "PAGEIND":"Consumer",
    "PERSISTENT":"IT",         "PETRONET":"Energy",           "PIDILITIND":"Chemicals",
    "PIIND":"Chemicals",       "PNB":"Banking",               "RECLTD":"Finance",
    "SIEMENS":"Capital Goods", "SRF":"Chemicals",             "TORNTPHARM":"Pharma",
    "TRENT":"Retail",          "UNIONBANK":"Banking",         "VBL":"FMCG",
    "VEDL":"Metals",           "VOLTAS":"Capital Goods",      "ZOMATO":"Consumer",
    "ZYDUSLIFE":"Pharma",
}

ALL_SECTORS = sorted(set(STOCKS.values()))

# ─────────────────────────────────────────────
# HIGH-SPEED MULTI-THREADED DATA LOADER & CACHE
# ─────────────────────────────────────────────
CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
CACHE_FILE = os.path.join(CACHE_DIR, "stock_filter_cache.json")
CACHE_TTL = 3600 * 4  # 4 hours persistent snapshot TTL

TICKER_MAP = {
    "TATAMOTORS": "TMPV.NS",
    "ICICIPRU": "ICICIPRULI.NS",
    "ZOMATO": "ETERNAL.NS",
}

def get_ns_ticker(sym: str) -> str:
    return TICKER_MAP.get(sym, f"{sym}.NS")

def _fetch_single_stock(sym: str, sector: str, close_series: pd.Series, prev_series: pd.Series) -> dict:
    ns = get_ns_ticker(sym)
    try:
        price = float(close_series.get(ns, 0) or 0)
        p_prev = float(prev_series.get(ns, price) or price)
        chg = ((price - p_prev) / p_prev * 100) if p_prev else 0.0
        t = yf.Ticker(ns)

        hi52 = lo52 = mc = 0.0
        try:
            fi = t.fast_info
            hi52 = float(getattr(fi, "year_high", 0) or 0)
            lo52 = float(getattr(fi, "year_low", 0) or 0)
            mc = float(getattr(fi, "market_cap", 0) or 0) / 1e7
            if price <= 0:
                price = float(getattr(fi, "last_price", 0) or 0)
        except Exception:
            pass

        full = {}
        try:
            full = t.info or {}
        except Exception:
            pass

        pe = float(full.get("trailingPE") or 0)
        debt = float(full.get("totalDebt") or 0) / 1e7
        div = float(full.get("dividendYield") or 0) * 100
        roe = float(full.get("returnOnEquity") or 0) * 100
        beta = float(full.get("beta") or 0)
        name = full.get("longName") or full.get("shortName") or sym

        if price > 0:
            return {
                "Name": name, "Ticker": sym, "Sector": sector, "Price": round(price, 2),
                "Change%": round(chg, 2), "PE": round(pe, 2), "MarketCap": round(mc, 2),
                "Debt": round(debt, 2), "52W_High": round(hi52 or price, 2),
                "52W_Low": round(lo52 or price, 2), "DivYield": round(div, 2),
                "ROE": round(roe, 2), "Beta": round(beta, 2)
            }
    except Exception:
        pass
    return None

@st.cache_data(ttl=1800, show_spinner=False)
def load_data(force_live: bool = False) -> pd.DataFrame:
    # 1. Instant Disk Cache Retrieval
    if not force_live and os.path.exists(CACHE_FILE):
        try:
            file_age = time.time() - os.path.getmtime(CACHE_FILE)
            if file_age < CACHE_TTL:
                with open(CACHE_FILE, "r", encoding="utf-8") as f:
                    cache_payload = json.load(f)
                cached_rows = cache_payload.get("data", [])
                if cached_rows:
                    return pd.DataFrame(cached_rows)
        except Exception:
            pass

    # 2. Ultra-Fast Parallel Multi-Threaded Fetch with ThreadPoolExecutor
    ns_tickers = [get_ns_ticker(t) for t in STOCKS]
    with st.spinner("⚡ Accelerating multi-threaded screener engine..."):
        try:
            raw = yf.download(ns_tickers, period="5d", auto_adjust=True, progress=False, threads=True)
            close = raw["Close"].ffill().iloc[-1]
            prev  = raw["Close"].ffill().iloc[-2]
        except Exception:
            close = prev = pd.Series(dtype=float)

        rows = []
        with ThreadPoolExecutor(max_workers=24) as executor:
            futures = [executor.submit(_fetch_single_stock, sym, sector, close, prev) for sym, sector in STOCKS.items()]
            for f in as_completed(futures):
                res = f.result()
                if res:
                    rows.append(res)

    if rows:
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                json.dump({"timestamp": time.time(), "data": rows}, f, indent=2)
        except Exception:
            pass

    return pd.DataFrame(rows)

def fmt_cr(val):
    if val >= 1_00_000: return f"₹{val/1_00_000:.2f}L Cr"
    if val >= 1_000:    return f"₹{val/1_000:.1f}K Cr"
    return f"₹{val:,.0f} Cr"

# ─────────────────────────────────────────────
# PRESET DEFINITIONS
# Each preset is a dict of filter keys → (min, max) or special
# ─────────────────────────────────────────────
PRESETS = {
    "🔥 Low P/E":       {"pe_min": 0,   "pe_max": 15},
    "💰 Large Cap":     {"mc_min": 50000,"mc_max": None},
    "🏦 Mid Cap":       {"mc_min": 5000, "mc_max": 50000},
    "🌱 Small Cap":     {"mc_min": 0,    "mc_max": 5000},
    "✅ Debt Free":     {"debt_max": 100},
    "📈 High ROE":      {"roe_min": 20},
    "💸 Dividend":      {"div_min": 1.0},
    "🔁 Reset":         {},
}

# ─────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────
st.markdown('<div class="hero-title">🔬 Stock Filter & Screener</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Screen NIFTY 100 — type exact values or pick a quick preset.</div>', unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
force_live = st.session_state.pop("force_live_refresh", False)
df = load_data(force_live=force_live)
if df.empty:
    st.error("⚠ Unable to fetch stock data."); st.stop()
df = df[df["Price"] > 0].reset_index(drop=True)

# ─────────────────────────────────────────────
# PRESET CHIP HANDLER
# Clicking a preset button sets session state defaults for the inputs
# ─────────────────────────────────────────────
if "preset" not in st.session_state:
    st.session_state.preset = None

preset_cols = st.columns(len(PRESETS))
for i, (label, vals) in enumerate(PRESETS.items()):
    with preset_cols[i]:
        if st.button(label, use_container_width=True, key=f"preset_{i}"):
            st.session_state.preset = label if label != "🔁 Reset" else None
            # write preset values into session state for the number inputs
            for k in ["pe_min","pe_max","mc_min","mc_max","debt_min","debt_max",
                      "price_min","price_max","roe_min","div_min"]:
                st.session_state[k] = vals.get(k, None)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FILTER PANEL — number inputs (no sliders)
# ─────────────────────────────────────────────
def get_default(key, fallback):
    v = st.session_state.get(key, None)
    return float(v) if v is not None else fallback

st.markdown('<div class="filter-panel"><div class="section-label">⚙ Filter Parameters</div>', unsafe_allow_html=True)

row1 = st.columns(5)

with row1[0]:
    st.markdown('<span class="filter-group-label">💰 Price (₹)</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: price_min = st.number_input("Min", min_value=0.0, value=get_default("price_min", 0.0),    step=10.0, label_visibility="collapsed", key="n_price_min", format="%g")
    with cb: price_max = st.number_input("Max", min_value=0.0, value=get_default("price_max", 99999.0), step=10.0, label_visibility="collapsed", key="n_price_max", format="%g")

with row1[1]:
    st.markdown('<span class="filter-group-label">📈 P/E Ratio</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: pe_min = st.number_input("Min", min_value=0.0, value=get_default("pe_min", 0.0),   step=1.0, label_visibility="collapsed", key="n_pe_min", format="%g")
    with cb: pe_max = st.number_input("Max", min_value=0.0, value=get_default("pe_max", 200.0), step=1.0, label_visibility="collapsed", key="n_pe_max", format="%g")

with row1[2]:
    st.markdown('<span class="filter-group-label">🏦 Market Cap (₹ Cr)</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: mc_min = st.number_input("Min", min_value=0.0, value=get_default("mc_min", 0.0),      step=1000.0, label_visibility="collapsed", key="n_mc_min", format="%g")
    with cb: mc_max = st.number_input("Max", min_value=0.0, value=get_default("mc_max", 9999999.0), step=1000.0, label_visibility="collapsed", key="n_mc_max", format="%g")

with row1[3]:
    st.markdown('<span class="filter-group-label">🔴 Max Debt (₹ Cr)</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: debt_min = st.number_input("Min", min_value=0.0, value=get_default("debt_min", 0.0),      step=1000.0, label_visibility="collapsed", key="n_debt_min", format="%g")
    with cb: debt_max = st.number_input("Max", min_value=0.0, value=get_default("debt_max", 9999999.0), step=1000.0, label_visibility="collapsed", key="n_debt_max", format="%g")

with row1[4]:
    st.markdown('<span class="filter-group-label">📊 ROE (%) / Div Yield (%)</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: roe_min = st.number_input("ROE ≥", min_value=0.0, value=get_default("roe_min", 0.0), step=1.0, label_visibility="collapsed", key="n_roe_min", format="%g")
    with cb: div_min = st.number_input("Div ≥", min_value=0.0, value=get_default("div_min", 0.0), step=0.1, label_visibility="collapsed", key="n_div_min", format="%g")

st.markdown('<div class="mini-divider"></div>', unsafe_allow_html=True)

# ── SECTOR CHIPS (multiselect replacement) ──
st.markdown('<div class="preset-label">🏭 Sector</div>', unsafe_allow_html=True)
if "selected_sectors" not in st.session_state:
    st.session_state.selected_sectors = []

# Build multiselect with pills styling
sector_filter = st.multiselect(
    "Sectors", ALL_SECTORS, default=st.session_state.selected_sectors,
    placeholder="All sectors (click to filter)", label_visibility="collapsed",
    key="sector_ms"
)

# ── SORT + VIEW ──
sc1, sc2, sc3 = st.columns([2, 2, 2])
with sc1:
    sort_options = {
        "Market Cap ↓": ("MarketCap", False), "Market Cap ↑": ("MarketCap", True),
        "Price ↓":      ("Price",     False), "Price ↑":      ("Price",     True),
        "P/E ↓":        ("PE",        False), "P/E ↑":        ("PE",        True),
        "Change % ↓":   ("Change%",   False), "Change % ↑":   ("Change%",   True),
        "ROE ↓":        ("ROE",       False), "ROE ↑":        ("ROE",       True),
    }
    sort_by = st.selectbox("↕ Sort By", list(sort_options.keys()), label_visibility="visible")
with sc2:
    view_mode = st.radio("👁 View", ["Cards", "Table"], horizontal=True)
with sc3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.session_state["force_live_refresh"] = True
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)  # close filter-panel

# ─────────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────────
mask = (
    (df["Price"]     >= price_min) & (df["Price"]     <= price_max) &
    (df["MarketCap"] >= mc_min)    & (df["MarketCap"] <= mc_max)    &
    (df["Debt"]      >= debt_min)  & (df["Debt"]      <= debt_max)  &
    (df["ROE"]       >= roe_min)   &
    (df["DivYield"]  >= div_min)
)
pe_mask = (df["PE"] == 0) | ((df["PE"] >= pe_min) & (df["PE"] <= pe_max))
mask = mask & pe_mask
if sector_filter:
    mask = mask & df["Sector"].isin(sector_filter)

filtered = df[mask].copy()
sk, asc  = sort_options[sort_by]
filtered = filtered.sort_values(sk, ascending=asc).reset_index(drop=True)

# ─────────────────────────────────────────────
# RESULT HEADER
# ─────────────────────────────────────────────
active_preset = st.session_state.get("preset", None)
preset_txt = f' • <span style="color:#ffffff;font-size:13px;">{active_preset}</span>' if active_preset else ""
st.markdown(
    f'<div style="font-size:20px;font-weight:800;color:#e2e8f0;margin-bottom:16px;">'
    f'Results <span class="count-badge">{len(filtered)} / {len(df)} stocks</span>{preset_txt}</div>',
    unsafe_allow_html=True
)

# ─────────────────────────────────────────────
# CARD VIEW
# ─────────────────────────────────────────────
if view_mode == "Cards":
    if filtered.empty:
        st.markdown('<div class="empty-state">🔍<br><br>No stocks match your filters.<br>Try adjusting the values above.</div>', unsafe_allow_html=True)
    else:
        left, right = st.columns(2)
        left_cards = []
        right_cards = []
        for i, row in filtered.iterrows():
            chg     = row["Change%"]
            chg_cls = "chg-pos" if chg >= 0 else "chg-neg"
            chg_sym = "▲" if chg >= 0 else "▼"
            rng     = row["52W_High"] - row["52W_Low"]
            wk_pct  = max(0, min(100, ((row["Price"] - row["52W_Low"]) / rng * 100) if rng > 0 else 50))
            bar_col = "#22c55e" if wk_pct > 60 else "#fbbf24" if wk_pct > 35 else "#f87171"

            pe_disp   = f'{row["PE"]:.1f}×'      if row["PE"]       > 0 else "N/A"
            debt_disp = fmt_cr(row["Debt"])       if row["Debt"]     > 0 else "Debt Free ✓"
            roe_disp  = f'{row["ROE"]:.1f}%'      if row["ROE"]     != 0 else "—"
            div_disp  = f'{row["DivYield"]:.2f}%' if row["DivYield"] > 0 else "—"

            card = f"""
            <div class="stock-card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>
                  <span class="s-name">{row['Name']}</span>
                  <span class="s-sym">{row['Ticker']}</span>
                  <div style="font-size:11px;color:var(--muted);margin-top:4px;">🏭 {row['Sector']}</div>
                </div>
                <div style="text-align:right;">
                  <div class="s-price">₹{row['Price']:,.2f}</div>
                  <div class="{chg_cls}">{chg_sym} {abs(chg):.2f}%</div>
                </div>
              </div>
              <div style="margin-top:10px;">
                <div style="display:flex;justify-content:space-between;font-size:10px;color:#6b7280;margin-bottom:3px;">
                  <span>52W Low ₹{row['52W_Low']:,.0f}</span>
                  <span>52W High ₹{row['52W_High']:,.0f}</span>
                </div>
                <div class="wk-track">
                  <div style="height:100%;width:{wk_pct:.1f}%;border-radius:2px;background:{bar_col};"></div>
                </div>
              </div>
              <div class="stat-row">
                <div class="stat-badge">P/E <b>{pe_disp}</b></div>
                <div class="stat-badge">Mkt Cap <b>{fmt_cr(row['MarketCap'])}</b></div>
                <div class="stat-badge">Debt <b>{debt_disp}</b></div>
                <div class="stat-badge">ROE <b>{roe_disp}</b></div>
                <div class="stat-badge">Div <b>{div_disp}</b></div>
                <div class="stat-badge">Beta <b>{row['Beta']:.2f}</b></div>
              </div>
            </div>"""
            (left_cards if i % 2 == 0 else right_cards).append(card)

        left.markdown("".join(left_cards), unsafe_allow_html=True)
        right.markdown("".join(right_cards), unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TABLE VIEW
# ─────────────────────────────────────────────
else:
    if filtered.empty:
        st.warning("⚠ No stocks match your filters.")
    else:
        disp = filtered[["Ticker","Name","Sector","Price","Change%","PE","MarketCap","Debt","ROE","DivYield","Beta"]].copy()
        disp["Price"]     = disp["Price"].apply(lambda x: f"₹{x:,.2f}")
        disp["Change%"]   = disp["Change%"].apply(lambda x: f"{'▲' if x>=0 else '▼'} {abs(x):.2f}%")
        disp["PE"]        = disp["PE"].apply(lambda x: f"{x:.1f}×" if x > 0 else "N/A")
        disp["MarketCap"] = disp["MarketCap"].apply(fmt_cr)
        disp["Debt"]      = disp["Debt"].apply(lambda x: fmt_cr(x) if x > 0 else "Debt Free ✓")
        disp["ROE"]       = disp["ROE"].apply(lambda x: f"{x:.1f}%" if x != 0 else "—")
        disp["DivYield"]  = disp["DivYield"].apply(lambda x: f"{x:.2f}%" if x > 0 else "—")
        disp["Beta"]      = disp["Beta"].apply(lambda x: f"{x:.2f}")
        disp.columns      = ["Ticker","Company","Sector","Price","Chg%","P/E","Mkt Cap","Debt","ROE","Div Yield","Beta"]
        st.dataframe(disp, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────
if not filtered.empty:
    st.divider()
    import io
    buf = io.BytesIO()
    filtered.to_csv(buf, index=False)
    ec1, ec2, ec3 = st.columns([3, 2, 3])
    with ec2:
        st.download_button("⬇ Export Results as CSV", buf.getvalue(),
                           "apex_filtered.csv", "text/csv", use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.caption("© 2026 Apex Stock Screener • Data via Yahoo Finance • Cached for 1 hour")