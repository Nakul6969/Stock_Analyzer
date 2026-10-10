import streamlit as st

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="Apex IPO Dashboard",
    page_icon="icon.png",
    layout="wide"
)

import requests
import os
from dotenv import load_dotenv
from ui.sidebar import render_sidebar
from ui.styles import load_global_css

if not st.session_state.get("logged_in"):
    st.switch_page("合_Welcome.py")

load_global_css()
render_sidebar()

# ---------------- ENV ----------------
load_dotenv()
API_KEY = os.getenv("INDIAN_API_KEY")

URL = "https://stock.indianapi.in/ipo"
HEADERS = {"X-Api-Key": API_KEY}

# ---------------- LOGO HELPER ----------------
LOGO_DEV_PUBLIC_KEY = "pk_IklwgQWBS--r9KUZrBrY6g"

def get_ipo_logo(name: str):
    if not name:
        return ""
    safe_name = name.replace(" ", "%20")
    return f"https://img.logo.dev/name/{safe_name}?token={LOGO_DEV_PUBLIC_KEY}"

# ---------------- CSS ----------------
st.markdown("""
<style>
.ipo-header{
  display:flex;
  align-items:center;
  gap:14px;
  margin-bottom:10px;
}

.ipo-logo{
  width:48px;
  height:48px;
  border-radius:12px;
  background:rgba(255,255,255,0.08);
  padding:6px;
  object-fit:contain;
}

 .block-container {
            padding-top: 1rem;
        }
:root{
  --bg1:#0c0c0c;
  --bg2:#000000;
  --glass:rgba(255,255,255,0.06);
  --border:rgba(255,255,255,0.12);
  --accent:#22c55e;
  --accent2:#ffffff;
  --info:#ffffff;
  --success:#22c55e;
  --danger:#ef4444;
  --text:#e5e7eb;
  --muted:#9ca3af;
}

/* ================= APEX BLACK GRADIENT ================= */

:root{
  --bg1:#000000;
  --bg2:#0c0c0c;
  --bg3:#000000;
  --text:#e5e7eb;
}

/* ---------- MAIN APP ---------- */
.stApp{
  background:
    radial-gradient(
      1200px 600px at 15% 10%,
      rgba(255,255,255,0.035),
      transparent
    ),
    radial-gradient(
      1000px 500px at 85% 20%,
      rgba(255,255,255,0.025),
      transparent
    ),
    linear-gradient(
      180deg,
      var(--bg1) 0%,
      var(--bg2) 55%,
      var(--bg3) 100%
    );

  color: var(--text);
  font-family: Inter, system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  min-height:100vh;
}

/* ---------- REMOVE STREAMLIT WHITE PATCHES ---------- */
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"]{
  background:transparent !important;
}

/* ---------- SMOOTH LOAD ---------- */
.stApp{
  animation:fadeIn 0.6s ease;
}

@keyframes fadeIn{
  from{opacity:0;}
  to{opacity:1;}
}


.page-title{
  font-size:38px;
  font-weight:900;
  background: linear-gradient(90deg, #ffffff, #525252);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
}

.ipo-card{
  background:linear-gradient(180deg,var(--glass),rgba(255,255,255,0.02));
  border:1px solid var(--border);
  border-radius:20px;
  padding:22px;
  margin-bottom:20px;
  transition:all 0.35s ease;
}
.ipo-card:hover{
  transform:translateY(-6px);
  box-shadow:0 22px 50px rgba(0,0,0,0.45);
}

.ipo-title{
  font-size:22px;
  font-weight:800;
}

.badge{
  display:inline-block;
  padding:5px 14px;
  border-radius:999px;
  font-size:12px;
  font-weight:800;
  margin-top:8px;
}

.badge-upcoming{background:rgba(255,255,255,0.10);color:#ffffff;}
.badge-active{background:rgba(34,197,94,0.15);color:#22c55e;}
.badge-listed{background:rgba(168,85,247,0.15);color:#a855f7;}
.badge-closed{background:rgba(239,68,68,0.15);color:#ef4444;}

.meta{
  font-size:14px;
  color:var(--muted);
  margin-top:6px;
}
/* ================= IPO PREMIUM TABS ================= */

/* Tabs wrapper spacing */
div[data-testid="stTabs"],
.stTabs{
  margin-top:18px !important;
  margin-bottom:12px !important;
}

/* Tabs container */
div[data-testid="stTabs"] [data-baseweb="tab-list"],
.stTabs [data-baseweb="tab-list"]{
  display:flex !important;
  width: 100% !important;
  gap:10px !important;
  padding:8px !important;
  background:linear-gradient(
    180deg,
    rgba(255,255,255,0.05),
    rgba(255,255,255,0.02)
  ) !important;
  border:1px solid rgba(255,255,255,0.12) !important;
  border-radius:18px !important;
  backdrop-filter:blur(14px) !important;
}

/* Individual tab */
div[data-testid="stTabs"] [data-baseweb="tab"],
.stTabs [data-baseweb="tab"]{
  flex: 1 1 0% !important;
  justify-content: center !important;
  text-align: center !important;
  position:relative !important;
  padding:12px 22px !important;
  font-size:15px !important;
  font-weight:700 !important;
  letter-spacing:0.3px !important;
  color:var(--muted) !important;
  background:transparent !important;
  border-radius:14px !important;
  transition:all 0.3s cubic-bezier(.22,1,.36,1) !important;
}

/* Hover effect */
div[data-testid="stTabs"] [data-baseweb="tab"]:hover,
.stTabs [data-baseweb="tab"]:hover{
  color:white !important;
  background:rgba(255,255,255,0.06) !important;
}

/* Active tab */
div[data-testid="stTabs"] [aria-selected="true"],
.stTabs [aria-selected="true"]{
  color:white !important;
  background:rgba(255,255,255,0.08) !important;
  box-shadow:
    inset 0 0 0 1px rgba(255,255,255,0.30),
    0 0 18px rgba(255,255,255,0.15) !important;
}

/* Neon underline indicator */
div[data-testid="stTabs"] [aria-selected="true"]::after,
.stTabs [aria-selected="true"]::after{
  content:"";
  position:absolute;
  left:20%;
  bottom:-7px;
  width:60%;
  height:3px;
  border-radius:3px;
  background:linear-gradient(90deg,var(--accent),var(--accent2));
  box-shadow:0 0 14px rgba(255, 255, 255, 0.540);
}

/* ================= HARD KILL STREAMLIT TAB INDICATOR ================= */

div[data-testid="stTabs"] div[role="presentation"],
div[data-testid="stTabs"] [data-baseweb="tab-border"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [aria-hidden="true"],
.stTabs div[role="presentation"],
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"],
.stTabs [aria-hidden="true"] {
    display: none !important;
    background: transparent !important;
    height: 0 !important;
}

div[data-testid="stTabs"],
div[data-testid="stTabs"] *,
.stTabs,
.stTabs * {
    border-bottom: none !important;
}

/* Metric cards inside IPO Dashboard - prevent ellipsis truncation */
[data-testid="stMetric"] {
    padding: 12px 14px !important;
}
[data-testid="stMetricLabel"] {
    font-size: 11px !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}
[data-testid="stMetricValue"] {
    font-size: 16px !important;
    font-weight: 700 !important;
    white-space: normal !important;
    word-break: break-word !important;
    text-overflow: unset !important;
    overflow: visible !important;
    line-height: 1.35 !important;
}
[data-testid="stMetricValue"] > div {
    white-space: normal !important;
    word-break: break-word !important;
    text-overflow: unset !important;
    overflow: visible !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HELPERS ----------------

def format_pct(val):
    try:
        num = float(val)
        sign = "+" if num > 0 else ""
        return f"{sign}{num:.2f}%"
    except:
        return "—"

def safe(val, default="—"):
    return val if val not in [None, "", "null"] else default

def price(val):
    return f"₹ {val}" if val not in [None, "", "null"] else "—"

def status_badge(key):
    return {
        "upcoming": "badge badge-upcoming",
        "active": "badge badge-active",
        "listed": "badge badge-listed",
        "closed": "badge badge-closed"
    }.get(key, "badge")

# ---------------- HEADER ----------------
st.markdown('<div class="page-title">Apex Presents Indian IPO Dashboard</div>', unsafe_allow_html=True)
st.caption("Track upcoming, active, listed & closed IPOs with clean insights")

# ---------------- CACHED DATA FETCHING ----------------
@st.cache_data(ttl=300, show_spinner=False)
def fetch_ipos():
    try:
        response = requests.get(URL, headers=HEADERS, timeout=12)
        if response.status_code == 200:
            return response.json()
        return {}
    except Exception:
        return {}

data = fetch_ipos()

tabs = st.tabs(["🔥 Active","🍁 Listed","📅 Upcoming", "👉 Closed"])

# ======================================================
# RENDER FUNCTIONS (KEY IMPROVEMENT)
# ======================================================
def render_upcoming(ipo):
    type_str = "SME - IPO" if ipo.get("is_sme") else "Mainboard - IPO"

    c1, c2, c3 = st.columns([1.45, 1.0, 1.1])
    c1.metric("Price Band", f"{price(ipo.get('min_price'))} – {price(ipo.get('max_price'))}")
    c2.metric("Symbol", safe(ipo.get("symbol")))
    c3.metric("IPO Type", type_str)

    st.markdown(
        f"<div class='meta'>🗓️ Bidding: {safe(ipo.get('bidding_start_date'))} → {safe(ipo.get('bidding_end_date'))}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='meta'>Information : {safe(ipo.get('additional_text'))}</div>",
        unsafe_allow_html=True
    )

def render_active(ipo):
    type_str = "SME - IPO" if ipo.get("is_sme") else "Mainboard - IPO"

    c1, c2, c3, c4 = st.columns([1.45, 0.75, 1.05, 1.15])
    c1.metric("Price Band", f"{price(ipo.get('min_price'))} – {price(ipo.get('max_price'))}")
    c2.metric("Lot Size", safe(ipo.get("lot_size")))
    c3.metric("Symbol", safe(ipo.get("symbol")))
    c4.metric("IPO Type", type_str)

    st.markdown(
        f"<div class='meta'>⏳ Started on {safe(ipo.get('bidding_start_date'))}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='meta'>⏳ Closing on {safe(ipo.get('bidding_end_date'))}</div>",
        unsafe_allow_html=True
    )

def render_listed(ipo):
    type_str = "SME - IPO" if ipo.get("is_sme") else "Mainboard - IPO"

    c1, c2, c3, c4 = st.columns([1.1, 1.1, 1.0, 1.15])
    c1.metric("Issue Price", price(ipo.get("issue_price")))
    c2.metric("Listing Price", price(ipo.get("listing_price")))
    c3.metric("Listing Gain", format_pct(ipo.get("listing_gains")))
    c4.metric("IPO Type", type_str)

    st.markdown(
        f"<div class='meta'>📈 Listed on {safe(ipo.get('listing_date'))}</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        f"<div class='meta'>Information : {safe(ipo.get('additional_text'))}</div>",
        unsafe_allow_html=True
    )

def render_closed(ipo):
    type_str = "SME - IPO" if ipo.get("is_sme") else "Mainboard - IPO"

    c1, c2, c3 = st.columns([1.45, 1.0, 1.1])
    c1.metric("Price Band", f"{price(ipo.get('min_price'))} – {price(ipo.get('max_price'))}")
    c2.metric("Symbol", safe(ipo.get("symbol")))
    c3.metric("IPO Type", type_str)

    st.markdown(
        f"<div class='meta'>Information : {safe(ipo.get('additional_text'))}</div>",
        unsafe_allow_html=True
    )

# ======================================================
# TAB RENDERING
# ======================================================
render_map = {
    "active": render_active,
    "upcoming": render_upcoming,
    "listed": render_listed,
    "closed": render_closed
}

keys = ["active", "listed", "upcoming", "closed"]

for tab, key in zip(tabs, keys):
    with tab:
        ipos = data.get(key, [])
        if not ipos:
            st.info("No IPOs available")
            continue

        for ipo in ipos:
            logo = get_ipo_logo(ipo.get("name"))

            st.markdown(f"""
            <div class="ipo-card">
                <div class="ipo-header">
                    <img src="{logo}" class="ipo-logo">
                    <div>
                        <div class="ipo-title">{safe(ipo.get("name"))}</div>
                        <div class="{status_badge(key)}">{key.upper()}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

            render_map[key](ipo)

            st.markdown("</div>", unsafe_allow_html=True)


st.divider()
st.caption("© 2025 Apex Stock Screener • IPO Analytics • Built with Python & Streamlit")

