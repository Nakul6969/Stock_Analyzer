import streamlit as st
import requests
import os
from dotenv import load_dotenv
from ui.sidebar import render_sidebar
from ui.styles import load_global_css

# ======================================================
# PAGE CONFIG (MUST BE FIRST)

st.set_page_config(
    page_title="Apex Stock Screener | Market Movers",
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

if not API_KEY:
    st.error("API key not found.")
    st.stop()

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
st.markdown('<div class="page-title">Market Movers By Apex</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="page-subtitle">'
    'Separated top gaining and losing stocks with strong intraday movement.'
    '</div>',
    unsafe_allow_html=True
)
st.divider()
# ======================================================
# DATA FETCH
# ======================================================
@st.cache_data(ttl=60, show_spinner=False)
def fetch_movers():
    r = requests.get(f"{BASE_URL}/trending", headers=HEADERS, timeout=10)
    return r.json() if r.status_code == 200 else None

data = fetch_movers()
if not data:
    st.error("Failed to fetch data.")
    st.stop()

gainers = data.get("trending_stocks", {}).get("top_gainers", [])
losers = data.get("trending_stocks", {}).get("top_losers", [])

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


if not apply:
    st.info("ᯓ★ Apply filters to view stocks.")
    st.stop()

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

