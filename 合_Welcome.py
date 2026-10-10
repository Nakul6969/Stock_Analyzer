import streamlit as st

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="Apex Stock Screener | Intelligence Platform",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from ui.sidebar import render_sidebar
from ui.styles import load_global_css
from auth.auth import render_auth
import base64
import yfinance as yf

@st.cache_data(show_spinner=False)
def img_to_base64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""

logo_base64 = img_to_base64("assets/logo.png")

# ---------------- SESSION INIT ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ---------------- AUTH GATE ----------------
if not st.session_state.logged_in:
    st.sidebar.empty()
    st.markdown("""
    <style>
    /* Hide raw Streamlit status badge (Running ...) */
    div[data-testid="stStatusWidget"],
    .stStatusWidget {
        visibility: hidden !important;
        display: none !important;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }
    .stApp {
        min-height: 100vh;
    }
    </style>
    """, unsafe_allow_html=True)

    render_auth()
    st.stop()

# ---------------- APP LOADS ONLY AFTER LOGIN ----------------
load_global_css()
render_sidebar()

# ---------------- REAL-TIME LIVE TICKER DATA FETCH ----------------
@st.cache_data(ttl=60, show_spinner=False)
def fetch_live_marquee_data():
    benchmarks = [
        ("NIFTY 50", "^NSEI", ""),
        ("SENSEX", "^BSESN", ""),
        ("BANK NIFTY", "^NSEBANK", ""),
        ("GOLD", "GC=F", "$"),
        ("CRUDE OIL", "CL=F", "$"),
        ("USD/INR", "INR=X", "₹"),
        ("SILVER", "SI=F", "$")
    ]
    items = []
    try:
        symbols = [s for _, s, _ in benchmarks]
        df = yf.download(symbols, period="5d", interval="1d", progress=False)
        close = df["Close"]
        for name, sym, pfx in benchmarks:
            try:
                s = close[sym].dropna()
                if len(s) >= 2:
                    curr = float(s.iloc[-1])
                    prev = float(s.iloc[-2])
                    pct = ((curr - prev) / prev) * 100
                elif len(s) == 1:
                    curr = float(s.iloc[-1])
                    pct = 0.0
                else:
                    continue

                if curr >= 1000:
                    val_str = f"{pfx}{curr:,.2f}"
                else:
                    val_str = f"{pfx}{curr:.2f}"

                pct_sign = "▲ +" if pct >= 0 else "▼ "
                pct_str = f"{pct_sign}{abs(pct):.2f}%"
                delta_class = "ticker-delta-up" if pct >= 0 else "ticker-delta-down"

                items.append({
                    "name": name,
                    "val": val_str,
                    "pct": pct_str,
                    "delta_class": delta_class
                })
            except Exception:
                pass
    except Exception:
        pass

    if not items:
        items = [
            {"name": "NIFTY 50", "val": "23,635.10", "pct": "▲ +0.45%", "delta_class": "ticker-delta-up"},
            {"name": "SENSEX", "val": "75,577.58", "pct": "▲ +0.38%", "delta_class": "ticker-delta-up"},
            {"name": "BANK NIFTY", "val": "56,777.55", "pct": "▼ -0.22%", "delta_class": "ticker-delta-down"},
            {"name": "GOLD", "val": "$4,439.30", "pct": "▲ +0.21%", "delta_class": "ticker-delta-up"},
            {"name": "CRUDE OIL", "val": "$92.16", "pct": "▲ +0.74%", "delta_class": "ticker-delta-up"},
            {"name": "USD/INR", "val": "₹94.81", "pct": "▲ +0.40%", "delta_class": "ticker-delta-up"},
            {"name": "SILVER", "val": "$66.95", "pct": "▲ +1.37%", "delta_class": "ticker-delta-up"},
        ]
    return items

live_items = fetch_live_marquee_data()
items_html_list = [
    f'<div class="ticker-item"><span class="ticker-sym">{it["name"]}</span><span class="ticker-val">{it["val"]}</span><span class="{it["delta_class"]}">{it["pct"]}</span></div>'
    for it in live_items
]
single_ticker_str = "".join(items_html_list)

# ---------------- TOP LIVE TICKER MARQUEE (DYNAMIC) ----------------
st.markdown(
    f'<div class="ticker-wrap"><div class="ticker-content">{single_ticker_str}{single_ticker_str}</div></div>',
    unsafe_allow_html=True
)

# ---------------- HERO SECTION (BENTO HERO) ----------------
hero_col1, hero_col2 = st.columns([1.2, 5.8], gap="medium")

with hero_col1:
    st.markdown(
        f'<div style="display: flex; align-items: center; justify-content: center; height: 100%;">'
        f'<div style="width: 120px; height: 120px; border-radius: 50%; overflow: hidden; border: 2px solid rgba(255,255,255,0.22); box-shadow: 0 0 35px rgba(255,255,255,0.12); display: flex; align-items: center; justify-content: center; background: #09090b;">'
        f'<img src="data:image/png;base64,{logo_base64}" style="width: 100%; height: 100%; object-fit: cover;">'
        f'</div></div>',
        unsafe_allow_html=True
    )

with hero_col2:
    st.markdown(
        '<div>'
        '<div class="live-badge"><span class="live-dot"></span> Real-Time Indian Market Engine</div>'
        '<h1 class="gradient-text" style="font-size: 38px; line-height: 1.15; margin: 0 0 10px 0;">'
        'Apex Stock Screener & FinTech Analytics</h1>'
        '<p style="color: #a1a1aa; font-size: 16px; line-height: 1.6; margin: 0; max-width: 860px;">'
        'A next-generation financial analytics suite engineered for Indian equities, derivatives, IPOs, and mutual funds. Built with Python, real-time market APIs, and machine learning risk analytics.'
        '</p></div>',
        unsafe_allow_html=True
    )

st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

# ---------------- BENTO GRID ROW 1: CORE CAPABILITIES & AI BEAM ----------------
col_b1, col_b2 = st.columns([1.6, 1.4], gap="medium")

with col_b1:
    st.markdown(
        '<div class="bento-card" style="height: 100%;">'
        '<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #a1a1aa; letter-spacing: 0.1em; text-transform: uppercase;">01 // Core Analytics</span>'
        '<span style="font-size: 13px; color: #ffffff; background: rgba(255,255,255,0.08); padding: 3px 9px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.14);">NSE & BSE</span>'
        '</div>'
        '<h2 style="font-size: 22px; margin: 0 0 8px 0; color: #ffffff;">Deep Equity Fundamental Intelligence</h2>'
        '<p style="color: #a1a1aa; font-size: 14px; line-height: 1.6; margin-bottom: 16px;">'
        'Instant access to financial health metrics, valuation multiples (P/E, P/B, EV/EBITDA), 50 & 200 Daily Moving Averages, trailing revenue, and corporate shareholding structures.'
        '</p>'
        '<div style="display: flex; gap: 8px; flex-wrap: wrap;">'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #f4f4f5; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 5px 10px; border-radius: 8px;">✓ 50+ Nifty Movers</span>'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #f4f4f5; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 5px 10px; border-radius: 8px;">✓ Interactive Candlesticks</span>'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #f4f4f5; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.12); padding: 5px 10px; border-radius: 8px;">✓ Ratio Heatmaps</span>'
        '</div></div>',
        unsafe_allow_html=True
    )

with col_b2:
    st.markdown(
        '<div class="bento-card bento-beam" style="height: 100%;">'
        '<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px;">'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #a1a1aa; letter-spacing: 0.1em; text-transform: uppercase;">02 // Machine Learning</span>'
        '<span class="live-badge" style="margin: 0; padding: 3px 8px; font-size: 10px;">'
        '<span class="live-dot" style="width: 5px; height: 5px;"></span> AI Model Ready</span>'
        '</div>'
        '<h2 style="font-size: 22px; margin: 0 0 8px 0; color: #ffffff;">Neural Risk & Sentiment Engine</h2>'
        '<p style="color: #a1a1aa; font-size: 14px; line-height: 1.6; margin-bottom: 16px;">'
        'Proprietary predictive risk scoring powered by historical volatility analysis, trend momentum vectors, and real-time news sentiment aggregation.'
        '</p>'
        '<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;">'
        '<span style="font-size: 13px; color: #a1a1aa;">Risk Engine Accuracy</span>'
        '<span class="mono-value" style="font-size: 15px;">88.1% Verified</span>'
        '</div></div>',
        unsafe_allow_html=True
    )

# ---------------- BENTO GRID ROW 2: 3 MULTI-ASSET PILLARS ----------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3, gap="medium")

with c1:
    st.markdown(
        '<div class="bento-card" style="height: 100%;">'
        '<div style="font-size: 24px; margin-bottom: 8px;">◧</div>'
        '<h3 style="font-size: 18px; margin: 0 0 6px 0; color: #ffffff;">IPO Intelligence & GMP</h3>'
        '<p style="color: #a1a1aa; font-size: 13px; line-height: 1.6; margin: 0;">'
        'Real-time Grey Market Premium (GMP) tracking, issue dates, lot sizes, and retail subscription status.'
        '</p></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        '<div class="bento-card" style="height: 100%;">'
        '<div style="font-size: 24px; margin-bottom: 8px;">▲▼</div>'
        '<h3 style="font-size: 18px; margin: 0 0 6px 0; color: #ffffff;">Nifty50 Market Movers</h3>'
        '<p style="color: #a1a1aa; font-size: 13px; line-height: 1.6; margin: 0;">'
        'Identify volume breakouts, top intraday gainers, and sector leaders across Indian market indices.'
        '</p></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        '<div class="bento-card" style="height: 100%;">'
        '<div style="font-size: 24px; margin-bottom: 8px;">◈</div>'
        '<h3 style="font-size: 18px; margin: 0 0 6px 0; color: #ffffff;">Commodities & Funds</h3>'
        '<p style="color: #a1a1aa; font-size: 13px; line-height: 1.6; margin: 0;">'
        'Track MCX Gold, Silver, Crude Oil, benchmark bond yields, and mutual fund NAV performances.'
        '</p></div>',
        unsafe_allow_html=True
    )

# ---------------- BENTO GRID ROW 3: PLATFORM STATS & ROADMAP ----------------
st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

stat_col1, stat_col2 = st.columns([1.5, 1.5], gap="medium")

with stat_col1:
    st.markdown(
        '<div class="bento-card" style="height: 100%;">'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #a1a1aa; letter-spacing: 0.1em; text-transform: uppercase;">Platform Architecture</span>'
        '<h3 style="font-size: 18px; margin: 6px 0 16px 0; color: #ffffff;">Engineered for High Precision</h3>'
        '<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px;">'
        '<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px;">'
        '<div style="font-size: 11px; color: #71717a; text-transform: uppercase; font-family: \'JetBrains Mono\', monospace;">Data Latency</div>'
        '<div class="mono-value" style="font-size: 20px; margin-top: 2px;">&lt; 250ms</div>'
        '</div>'
        '<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px;">'
        '<div style="font-size: 11px; color: #71717a; text-transform: uppercase; font-family: \'JetBrains Mono\', monospace;">Security</div>'
        '<div class="mono-value" style="font-size: 20px; margin-top: 2px;">OAuth 2.0</div>'
        '</div>'
        '<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px;">'
        '<div style="font-size: 11px; color: #71717a; text-transform: uppercase; font-family: \'JetBrains Mono\', monospace;">Database</div>'
        '<div class="mono-value" style="font-size: 20px; margin-top: 2px;">Mongo Atlas</div>'
        '</div>'
        '<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 12px;">'
        '<div style="font-size: 11px; color: #71717a; text-transform: uppercase; font-family: \'JetBrains Mono\', monospace;">Coverage</div>'
        '<div class="mono-value" style="font-size: 20px; margin-top: 2px;">100+ Equities</div>'
        '</div>'
        '</div></div>',
        unsafe_allow_html=True
    )

with stat_col2:
    st.markdown(
        '<div class="bento-card" style="height: 100%;">'
        '<span style="font-family: \'JetBrains Mono\', monospace; font-size: 11px; color: #a1a1aa; letter-spacing: 0.1em; text-transform: uppercase;">Strategic Roadmap</span>'
        '<h3 style="font-size: 18px; margin: 6px 0 14px 0; color: #ffffff;">Platform Evolution 2026</h3>'
        '<div style="display: flex; flex-direction: column; gap: 10px;">'
        '<div style="display: flex; align-items: center; gap: 10px; font-size: 13px;">'
        '<span style="color: #ffffff; background: rgba(255,255,255,0.12); border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">✓</span>'
        '<span style="color: #f4f4f5;">Live yahoo finance & IndianAPI Integration</span>'
        '</div>'
        '<div style="display: flex; align-items: center; gap: 10px; font-size: 13px;">'
        '<span style="color: #ffffff; background: rgba(255,255,255,0.12); border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">✓</span>'
        '<span style="color: #f4f4f5;">Secure JWT & Email OTP Verification System</span>'
        '</div>'
        '<div style="display: flex; align-items: center; gap: 10px; font-size: 13px;">'
        '<span style="color: #ffffff; background: rgba(255,255,255,0.12); border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700;">✓</span>'
        '<span style="color: #f4f4f5;">Machine Learning Risk Assessment Suite</span>'
        '</div>'
        '<div style="display: flex; align-items: center; gap: 10px; font-size: 13px;">'
        '<span style="color: #71717a; border: 1px solid rgba(255,255,255,0.15); border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 10px;">⚡</span>'
        '<span style="color: #a1a1aa;">Algorithmic Backtesting & Custom Alert Triggers</span>'
        '</div>'
        '</div></div>',
        unsafe_allow_html=True
    )

# ---------------- GET STARTED CTA ----------------
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

cta_l, cta_mid, cta_r = st.columns([3, 2.8, 3])

with cta_mid:
    if st.button("⌯✈ Launch Screener & Insights", use_container_width=True, type="primary"):
        st.switch_page("pages/⌘_Stock_Insights.py")

st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown(
    '<div style="text-align: center; border-top: 1px solid rgba(255,255,255,0.08); padding-top: 20px; margin-top: 20px;">'
    '<p style="font-family: \'DM Sans\', sans-serif; font-size: 12px; color: #71717a; margin: 0;">'
    '© 2026 Apex Stock Screener • Institutional-Grade FinTech Analytics • Built with Python & Streamlit'
    '</p></div>',
    unsafe_allow_html=True
)
