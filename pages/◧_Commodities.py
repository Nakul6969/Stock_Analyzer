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
