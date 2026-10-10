# Gold, Silver, Copper, Zinc → Metals
# Crude Oil, Natural Gas → Energy
# Cotton, Soybean, Mentha → Agri
# Else → Others

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from ui.sidebar import render_sidebar
from ui.styles import load_global_css

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Apex Commodities Dashboard",
    page_icon="icon.png",
    layout="wide"
)

if not st.session_state.get("logged_in"):
    st.switch_page("合_Welcome.py")

load_global_css()
render_sidebar()

# ======================================================
# ENV & API
# ======================================================
load_dotenv()
API_KEY = os.getenv("INDIAN_API_KEY")
URL = "https://stock.indianapi.in/commodities"
HEADERS = {"X-Api-Key": API_KEY}

if not API_KEY:
    st.error("API key not found")
    st.stop()

# ======================================================
# PAGE CSS (LIGHTWEIGHT – GLOBAL CSS ALREADY APPLIED)
# ======================================================
st.markdown("""
<style>
/* ================= APEX PREMIUM TABS (IPO STYLE) ================= */

/* Tabs wrapper spacing */
.stTabs{
  margin-top:18px;
  margin-bottom:14px;
}

/* Tabs container */
.stTabs [data-baseweb="tab-list"]{
  display:flex;
  gap:10px;
  padding:8px;
  background:linear-gradient(
    180deg,
    rgba(255,255,255,0.05),
    rgba(255,255,255,0.02)
  );
  border:1px solid rgba(255,255,255,0.12);
  border-radius:18px;
  backdrop-filter:blur(14px);
}

/* Individual tab */
.stTabs [data-baseweb="tab"]{
  position:relative;
  padding:12px 22px;
  font-size:15px;
  font-weight:700;
  letter-spacing:0.3px;
  color:#9ca3af;
  background:transparent;
  border-radius:14px;
  transition:all 0.3s cubic-bezier(.22,1,.36,1);
}

/* Hover */
.stTabs [data-baseweb="tab"]:hover{
  color:white;
  background:rgba(255,255,255,0.06);
}

/* Active tab */
.stTabs [aria-selected="true"]{
  color:white !important;
  background:rgba(255,255,255,0.08);
  box-shadow:
    inset 0 0 0 1px rgba(255,255,255,0.30),
    0 0 18px rgba(255,255,255,0.15);
}

/* Neon underline */
.stTabs [aria-selected="true"]::after{
  content:"";
  position:absolute;
  left:20%;
  bottom:-7px;
  width:60%;
  height:3px;
  border-radius:3px;
  background:linear-gradient(90deg,#22c55e,#ffffff);
  box-shadow:0 0 14px rgba(255, 255, 255, 0.540);
}

/* Remove default underline */
.stTabs [data-baseweb="tab-border"]{
  display:none;
}

.page-title{
  font-size:36px;
  font-weight:900;
  background: linear-gradient(90deg, #ffffff, #525252);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

.glass{
  background:linear-gradient(180deg,rgba(255,255,255,0.06),rgba(255,255,255,0.02));
  border:1px solid rgba(255,255,255,0.12);
  border-radius:20px;
  padding:20px;
  margin-bottom:18px;
}

.product{ font-size:20px; font-weight:800; }
.meta{ font-size:13px; color:#9ca3af; margin-top:6px; }

.gain{ color:#22c55e; font-weight:800; }
.loss{ color:#ef4444; font-weight:800; }

.badge{
  display:inline-block;
  padding:6px 14px;
  border-radius:999px;
  font-size:12px;
  font-weight:800;
  margin-top:10px;
  background:rgba(255,255,255,0.10);
  color:#ffffff;
}
/* ================= EQUAL-WIDTH TABS ================= */

/* Tab list container */
.stTabs [data-baseweb="tab-list"]{
  display: flex;
  width: 100%;
}

/* Each tab takes equal space */
.stTabs [data-baseweb="tab"]{
  flex: 1 1 0%;
  text-align: center;
}
/* ================= HARD KILL STREAMLIT TAB INDICATOR ================= */

/* Kill BaseWeb animated indicator */
.stTabs div[role="presentation"] {
    display: none !important;
    height: 0 !important;
    background: transparent !important;
}

/* Extra safety: any leftover underline */
.stTabs [data-baseweb="tab-border"],
.stTabs [aria-hidden="true"] {
    display: none !important;
    background: transparent !important;
    height: 0 !important;
}

/* Ensure no bottom borders anywhere */
.stTabs,
.stTabs * {
    border-bottom: none !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HELPERS
# ======================================================
def safe(v, d="—"):
    return v if v not in [None, "", "NULL"] else d

def price(v):
    return f"₹ {v}" if v not in [None, "", "NULL"] else "—"

def pct(v):
    try:
        return float(v)
    except:
        return 0.0

# ======================================================
# CATEGORY MAPPER (KEY PART)
# ======================================================
def get_category(product):
    p = product.lower()
    if any(x in p for x in ["gold", "silver", "copper", "zinc", "lead", "aluminium"]):
        return "🪙 Metals"
    if any(x in p for x in ["crude", "natural gas"]):
        return "⚡ Energy"
    if any(x in p for x in ["cotton", "soy", "soybean", "mentha", "guar", "jeera"]):
        return "🌾 Agri"
    return "🧪 Others"

# ======================================================
# HEADER
# ======================================================
st.markdown('<div class="page-title">📦 Commodities Dashboard</div>', unsafe_allow_html=True)
st.caption("Live MCX commodities prices, trends & open interest insights")

# ======================================================
# FETCH DATA
# ======================================================
@st.cache_data(ttl=60, show_spinner=False)
def fetch_commodities():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    return r.json() if r.status_code == 200 else []

data = fetch_commodities()

if not data:
    st.warning("No commodities data available")
    st.stop()

# ======================================================
# GROUP BY CATEGORY → PRODUCT
# ======================================================
categories = {}

for item in data:
    product = item.get("product", "UNKNOWN")
    category = get_category(product)

    categories.setdefault(category, {})
    categories[category].setdefault(product, []).append(item)

# ======================================================
# RENDER TABS (CATEGORY-WISE)
# ======================================================

tabs = st.tabs(list(categories.keys()))


for tab, (category, products) in zip(tabs, categories.items()):
    with tab:
        for product, items in products.items():
            st.subheader(product)

            cols = st.columns(3)
            for i, item in enumerate(items):
                with cols[i % 3]:
                    change = pct(item.get("per_change"))
                    cls = "gain" if change >= 0 else "loss"

                    st.markdown(f"""
                    <div class="glass">
                      <div class="product">{product}</div>
                      <div class="meta">
                        {safe(item.get("product_month"))}
                        • Exp: {safe(item.get("expiry"))}
                      </div>

                      <br>
                      <div><b>Last Price:</b> {price(item.get("last_traded_price"))}</div>
                      <div class="{cls}">{change:+.2f}%</div>

                      <div class="meta">
                        High / Low:
                        {price(item.get("high_price"))}
                        /
                        {price(item.get("low_price"))}
                      </div>

                      <div class="meta">
                        Open Interest: {safe(item.get("open_interest"))}
                      </div>

                      <div class="meta">
                        OI Trend: {safe(item.get("oiResult"))}
                      </div>

                      <div class="badge">
                        {safe(item.get("price_quotation_unit"))}
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

            st.divider()

# ======================================================
# FOOTER
# ======================================================

st.caption("© 2025 Apex Stock Screener • Commodities Analytics • Built with Python & Streamlit")
