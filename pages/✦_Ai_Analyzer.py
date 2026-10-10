import streamlit as st

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="Apex AI Financial Copilot · Risk Intelligence",
    page_icon="icon.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from ui.styles import load_global_css
from ui.sidebar import render_sidebar
from auth.auth import render_auth
from ml.predict import fetch_and_predict
import math

@st.cache_data(ttl=300, show_spinner=False)
def analyze_stock_cached(symbol: str) -> dict:
    """Cached stock analysis to avoid redundant network calls within 5 minutes."""
    return fetch_and_predict(symbol)

if not st.session_state.get("logged_in"):
    render_auth()
    st.stop()

load_global_css()
render_sidebar()

# ─────────────────────────────────────────────
# AI CHATBOT INTERFACE STYLING (OBSIDIAN & PLATINUM)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700;800&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, sans-serif;
}

/* ── Chat Header Banner ── */
.ai-copilot-header {
    background: linear-gradient(180deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.015) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 20px;
    padding: 22px 28px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
    backdrop-filter: blur(16px);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}
.ai-copilot-header::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
}
.ai-brand-group {
    display: flex;
    align-items: center;
    gap: 16px;
}
.ai-avatar-orb {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
    color: #000000;
    font-size: 22px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 24px rgba(255, 255, 255, 0.35);
    flex-shrink: 0;
}
.ai-header-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: #ffffff;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.ai-header-sub {
    font-size: 13px;
    color: #a1a1aa;
    margin-top: 4px;
}
.ai-model-pill {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 999px;
    padding: 6px 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #f4f4f5;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.ai-model-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #22c55e;
    box-shadow: 0 0 8px #22c55e;
    animation: pulseRadar 2s infinite ease-in-out;
}

/* ── Chat Timeline Layout ── */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    margin-bottom: 28px;
}

/* User Message */
.chat-row-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 14px;
}
.chat-bubble-user {
    background: rgba(255, 255, 255, 0.07);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 18px 18px 4px 18px;
    padding: 12px 20px;
    color: #ffffff;
    max-width: 65%;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
.chat-sender-user {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: #a1a1aa;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.chat-content-user {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
    letter-spacing: 0.01em;
}

/* Bot Message */
.chat-row-bot {
    display: flex;
    align-items: flex-start;
    gap: 14px;
    margin-bottom: 24px;
}
.chat-avatar-bot-sm {
    width: 36px;
    height: 36px;
    border-radius: 11px;
    background: #ffffff;
    color: #000000;
    font-size: 16px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 16px rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
    margin-top: 4px;
}
.chat-bubble-bot {
    background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.015) 100%);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 4px 20px 20px 20px;
    padding: 18px 22px;
    color: #f4f4f5;
    flex: 1;
    max-width: 780px;
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(14px);
}
.chat-sender-bot {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}
.chat-sender-tag {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.12);
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 9px;
    color: #a1a1aa;
}

/* ── Chatbot Input & Action Controls ── */
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] [data-baseweb="base-input"],
div[data-testid="stTextInput"] [data-baseweb="input"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] input {
    background: #09090b !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
    height: 48px !important;
    padding: 0 18px !important;
    transition: all 0.25s ease !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(255,255,255,0.45) !important;
    box-shadow: 0 0 16px rgba(255, 255, 255, 0.12) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #71717a !important;
}
div[data-testid="stTextInput"] label {
    display: none !important;
}

/* ── Crisp Pure White Action Button (Request 3) ── */
div.st-key-ai_analyze_btn button,
div[data-testid="stButton"] button {
    height: 48px !important;
    width: 100% !important;
    border-radius: 14px !important;
    background: #ffffff !important;
    border: 1px solid #ffffff !important;
    color: #000000 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 800 !important;
    font-size: 15px !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.25) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}
div.st-key-ai_analyze_btn button:hover,
div[data-testid="stButton"] button:hover {
    background: #e4e4e7 !important;
    color: #000000 !important;
    border-color: #ffffff !important;
    box-shadow: 0 0 30px rgba(255, 255, 255, 0.50) !important;
    transform: translateY(-2px) !important;
}
div.st-key-ai_analyze_btn button:active,
div[data-testid="stButton"] button:active {
    transform: translateY(0) !important;
}

/* ── Clear Thread Button (Secondary) ── */
div.st-key-ai_clear_btn button {
    height: 48px !important;
    border-radius: 14px !important;
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    color: #a1a1aa !important;
    font-size: 13px !important;
    font-weight: 600 !important;
    box-shadow: none !important;
}
div.st-key-ai_clear_btn button:hover {
    background: rgba(239, 68, 68, 0.15) !important;
    border-color: rgba(239, 68, 68, 0.35) !important;
    color: #ef4444 !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Quick Prompt Chips Row ── */
.ai-chips-wrapper {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
    margin-bottom: 24px;
}
.ai-chips-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #71717a;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-right: 6px;
}

/* ── Welcome Empty State ── */
.ai-welcome-box {
    text-align: center;
    padding: 50px 20px;
    background: linear-gradient(180deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.01) 100%);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 22px;
    margin-bottom: 28px;
}
.ai-welcome-icon {
    font-size: 38px;
    margin-bottom: 14px;
    color: #ffffff;
    text-shadow: 0 0 20px rgba(255,255,255,0.5);
}
.ai-welcome-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 8px;
}
.ai-welcome-desc {
    font-size: 14px;
    color: #a1a1aa;
    max-width: 580px;
    margin: 0 auto 24px auto;
    line-height: 1.6;
}
.ai-welcome-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
    max-width: 760px;
    margin: 0 auto;
}
.ai-welcome-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 14px;
    padding: 14px 16px;
    text-align: left;
    transition: all 0.2s ease;
}
.ai-welcome-card:hover {
    border-color: rgba(255, 255, 255, 0.25);
    background: rgba(255, 255, 255, 0.05);
}
.ai-welcome-card-title {
    font-size: 13px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 4px;
}
.ai-welcome-card-sub {
    font-size: 11px;
    color: #71717a;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# GAUGE GENERATOR (COMPACT HIGH-DPI SVG)
# ─────────────────────────────────────────────
def render_gauge(score: float) -> str:
    pct = max(0.0, min(1.0, (score - 1.0) / 9.0))
    th = math.radians(180.0 - pct * 180.0)
    nx = 48.0 + 26.0 * math.cos(th)
    ny = 48.0 - 26.0 * math.sin(th)
    return (
        f'<svg width="92" height="52" viewBox="0 0 96 54" style="overflow:visible;display:block;">'
        f'<path d="M 12 48 A 36 36 0 0 1 84 48" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="6" stroke-linecap="round"/>'
        f'<path d="M 12 48 A 36 36 0 0 1 30 16.8" fill="none" stroke="#22c55e" stroke-width="5.5" opacity="0.85"/>'
        f'<path d="M 30 16.8 A 36 36 0 0 1 66 16.8" fill="none" stroke="#f59e0b" stroke-width="5.5" opacity="0.85"/>'
        f'<path d="M 66 16.8 A 36 36 0 0 1 84 48" fill="none" stroke="#ef4444" stroke-width="5.5" opacity="0.85"/>'
        f'<line x1="48" y1="48" x2="{nx:.1f}" y2="{ny:.1f}" stroke="#ffffff" stroke-width="2" stroke-linecap="round"/>'
        f'<circle cx="48" cy="48" r="3.5" fill="#ffffff"/>'
        f'<circle cx="48" cy="48" r="1.5" fill="#09090b"/>'
        f'<text x="10" y="54" fill="#22c55e" font-size="6.5" font-family="JetBrains Mono,monospace" text-anchor="middle" font-weight="700">LOW</text>'
        f'<text x="48" y="8" fill="#f59e0b" font-size="6.5" font-family="JetBrains Mono,monospace" text-anchor="middle" font-weight="700">MED</text>'
        f'<text x="86" y="54" fill="#ef4444" font-size="6.5" font-family="JetBrains Mono,monospace" text-anchor="middle" font-weight="700">HIGH</text>'
        f'</svg>'
    )

# ─────────────────────────────────────────────
# LUXURY OBSIDIAN RISK DIAGNOSTIC CARD (COMPACT DUAL-COLUMN)
# ─────────────────────────────────────────────
def render_result_card(result: dict) -> str:
    score   = result["score"]
    fv      = result["features"]
    signals = result["signals"]
    gauge   = render_gauge(score)

    if score <= 3.5:
        zc = "#22c55e"; zbg = "rgba(34,197,94,0.12)";  zbd = "rgba(34,197,94,0.30)"
        verdict_badge = "LOW RISK"
    elif score <= 6.5:
        zc = "#f59e0b"; zbg = "rgba(245,158,11,0.12)"; zbd = "rgba(245,158,11,0.30)"
        verdict_badge = "BALANCED RISK"
    else:
        zc = "#ef4444"; zbg = "rgba(239,68,68,0.12)";  zbd = "rgba(239,68,68,0.30)"
        verdict_badge = "ELEVATED RISK"

    pills = ""
    for sl, st_ in signals[:4]:
        bg  = "rgba(34,197,94,0.10)"  if st_ == "ok" else "rgba(245,158,11,0.10)" if st_ == "warn" else "rgba(239,68,68,0.10)"
        clr = "#22c55e"               if st_ == "ok" else "#f59e0b"               if st_ == "warn" else "#ef4444"
        bdr = "rgba(34,197,94,0.25)"  if st_ == "ok" else "rgba(245,158,11,0.25)" if st_ == "warn" else "rgba(239,68,68,0.25)"
        icon = "✓ " if st_ == "ok" else "⚠ "
        pills += (
            f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:9.5px;font-weight:600;'
            f'padding:2px 7px;border-radius:10px;background:{bg};color:{clr};border:1px solid {bdr};">{icon}{sl}</span>'
        )

    pec   = "#ef4444" if fv["pe_ratio"] > 35 else "#22c55e"
    betac = "#ef4444" if fv["beta"] > 1.2 else "#22c55e"
    dec   = "#ef4444" if fv["debt_equity"] > 1.0 else "#22c55e"
    mgc   = "#22c55e" if fv["net_margin"] > 12 else "#f59e0b"
    d50c  = "#22c55e" if fv["dma50_ratio"] >= 1 else "#ef4444"
    chgc  = "#22c55e" if fv["price_52w_change"] > 0 else "#ef4444"

    def mini_cell(lbl, val, sub, sc):
        return (
            f'<div style="background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.06);border-radius:8px;padding:6px 8px;">'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:9px;color:#71717a;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:2px;">{lbl}</div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:700;color:#ffffff;line-height:1.2;">{val}</div>'
            f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:9px;font-weight:600;color:{sc};margin-top:2px;">{sub}</div>'
            f'</div>'
        )

    grid = (
        mini_cell("P/E Ratio",   f"{fv['pe_ratio']:.1f}",           "Elevated" if fv['pe_ratio'] > 35 else "Healthy", pec) +
        mini_cell("Beta",        f"{fv['beta']:.2f}",               "High Vol" if fv['beta'] > 1.2 else "Stable",    betac) +
        mini_cell("Debt / Eq",   f"{fv['debt_equity']:.2f}",        "Leveraged" if fv['debt_equity'] > 1.0 else "Low Lev", dec) +
        mini_cell("Net Margin",  f"{fv['net_margin']:.1f}%",        "Strong" if fv['net_margin'] > 12 else "Moderate", mgc) +
        mini_cell("50 DMA",      f"{fv['dma50_ratio']:.2f}x",       "Above DMA" if fv['dma50_ratio'] >= 1 else "Below DMA", d50c) +
        mini_cell("52W Return",  f"{fv['price_52w_change']:+.1f}%", "Positive" if fv['price_52w_change'] > 0 else "Negative", chgc)
    )

    card = (
        f'<div style="background:linear-gradient(180deg, rgba(20,20,24,0.95) 0%, rgba(12,12,16,0.95) 100%);border:1px solid rgba(255,255,255,0.10);border-radius:14px;overflow:hidden;box-shadow:0 8px 30px rgba(0,0,0,0.45);margin-top:10px;max-width:640px;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;padding:9px 14px;background:rgba(255,255,255,0.02);border-bottom:1px solid rgba(255,255,255,0.06);">'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:14px;color:#ffffff;">{result["stock_name"]}</span>'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#a1a1aa;background:rgba(255,255,255,0.06);padding:2px 6px;border-radius:4px;">{result["ticker"]}</span>'
        f'</div>'
        f'<div style="display:flex;align-items:center;gap:10px;font-family:\'JetBrains Mono\',monospace;">'
        f'<span style="font-size:13px;font-weight:700;color:#ffffff;">₹{result["current_price"]:,.2f}</span>'
        f'<span style="font-size:10px;color:#71717a;">52W: ₹{result["year_low"]:,.0f} - ₹{result["year_high"]:,.0f}</span>'
        f'</div>'
        f'</div>'
        f'<div style="display:flex;align-items:center;padding:12px 14px;gap:14px;">'
        f'<div style="flex-shrink:0;width:130px;display:flex;flex-direction:column;align-items:center;border-right:1px solid rgba(255,255,255,0.06);padding-right:12px;">'
        f'{gauge}'
        f'<div style="font-family:\'Space Grotesk\',sans-serif;font-size:24px;font-weight:800;line-height:1;color:{zc};margin-top:4px;">{score:.1f}<span style="font-size:11px;font-weight:500;color:#71717a;">/10</span></div>'
        f'<div style="display:inline-flex;align-items:center;gap:4px;background:{zbg};border:1px solid {zbd};border-radius:5px;padding:2px 7px;margin-top:4px;">'
        f'<span style="width:5px;height:5px;border-radius:50%;background:{zc};box-shadow:0 0 6px {zc};"></span>'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:9px;font-weight:700;color:{zc};letter-spacing:0.04em;">{verdict_badge}</span>'
        f'</div>'
        f'</div>'
        f'<div style="flex:1;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px;">{grid}</div>'
        f'</div>'
        f'<div style="border-top:1px solid rgba(255,255,255,0.06);padding:7px 14px;display:flex;align-items:center;gap:6px;flex-wrap:wrap;background:rgba(0,0,0,0.2);">'
        f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:9px;font-weight:700;color:#71717a;letter-spacing:0.06em;margin-right:2px;">SIGNALS:</span>'
        f'{pills}'
        f'</div>'
        f'<div style="border-top:1px solid rgba(255,255,255,0.06);padding:6px 14px;display:flex;justify-content:space-between;align-items:center;background:rgba(0,0,0,0.35);font-family:\'JetBrains Mono\',monospace;font-size:9px;color:#71717a;">'
        f'<div>MODEL: <span style="color:#ffffff">RandomForest v2.0 (17 Features)</span> • RISK: <span style="color:#ffffff">{result.get("api_risk_label","Standard")}</span></div>'
        f'<div style="color:#22c55e;">CONFIDENCE: HIGH</div>'
        f'</div>'
        f'</div>'
    )
    return card

# ─────────────────────────────────────────────
# CHATBOT HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="ai-copilot-header">
    <div class="ai-brand-group">
        <div class="ai-avatar-orb">✦</div>
        <div>
            <div class="ai-header-title">Apex AI Financial Copilot</div>
            <div class="ai-header-sub">Conversational Machine Learning Stock Risk Engine • Trained on 17 Institutional Metrics</div>
        </div>
    </div>
    <div class="ai-model-pill">
        <span class="ai-model-dot"></span>
        RandomForest Model v2.0 • Active
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session State Management ──
if "risk_messages" not in st.session_state:
    st.session_state.risk_messages = []
if "chat_input_val" not in st.session_state:
    st.session_state.chat_input_val = ""

# ─────────────────────────────────────────────
# INPUT ROW & ACTIONS
# ─────────────────────────────────────────────
c_input, c_btn, c_clear = st.columns([5, 1.4, 1])

with c_input:
    input_text = st.text_input(
        "Chat Input",
        value=st.session_state.chat_input_val,
        placeholder="Ask Apex AI about any Indian stock... (e.g. TCS, Reliance, Infosys, HDFC Bank)",
        key="main_stock_chat_input",
        label_visibility="collapsed"
    )

with c_btn:
    analyze_clicked = st.button("Analyze 🎯", key="ai_analyze_btn", use_container_width=True)

with c_clear:
    if st.button("🗑 Clear", key="ai_clear_btn", use_container_width=True):
        st.session_state.risk_messages = []
        st.session_state.chat_input_val = ""
        st.rerun()

# ─────────────────────────────────────────────
# QUICK PROMPT CHIPS
# ─────────────────────────────────────────────
st.markdown('<div class="ai-chips-wrapper"><span class="ai-chips-label">QUICK PROMPTS:</span>', unsafe_allow_html=True)
chip_cols = st.columns(6)
chips = [
    ("⚡ RELIANCE", "RELIANCE"),
    ("🎯 TCS", "TCS"),
    ("🏦 HDFC BANK", "HDFCBANK"),
    ("💻 INFOSYS", "INFY"),
    ("🚗 TATA MOTORS", "TATAMOTORS"),
    ("🛒 TRENT", "TRENT")
]

selected_chip = None
for i, (chip_label, ticker_code) in enumerate(chips):
    with chip_cols[i]:
        if st.button(chip_label, key=f"chip_{ticker_code}", use_container_width=True):
            selected_chip = ticker_code

st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EXECUTE ANALYSIS (PROMPT OR CHIP)
# ─────────────────────────────────────────────
target_symbol = None
if analyze_clicked and input_text.strip():
    target_symbol = input_text.strip()
elif selected_chip:
    target_symbol = selected_chip

if target_symbol:
    st.session_state.chat_input_val = ""
    # 1. Append User Message
    st.session_state.risk_messages.append({
        "role": "user",
        "content": f"Analyze risk profile, financial strength, and valuation for {target_symbol.upper()}"
    })

    # 2. Fetch ML Analysis & Append Bot Message
    with st.spinner(f"✦ Apex AI is analyzing {target_symbol.upper()} across 17 risk dimensions..."):
        try:
            result = analyze_stock_cached(target_symbol)
            card_html = render_result_card(result)
            score = result["score"]

            # Conversational Executive Synthesis
            if score <= 3.5:
                synth_verdict = f"<strong>{result['stock_name']} ({result['ticker']})</strong> reflects a <strong>Low-Risk</strong> institutional profile with superior financial health and manageable debt obligations."
            elif score <= 6.5:
                synth_verdict = f"<strong>{result['stock_name']} ({result['ticker']})</strong> shows a <strong>Balanced/Moderate Risk</strong> profile with stable operational cash flows and steady margins."
            else:
                synth_verdict = f"<strong>{result['stock_name']} ({result['ticker']})</strong> exhibits <strong>Elevated Volatility / Higher Risk</strong> with key sensitivities in moving averages or valuation multiples."

            synth_html = (
                f'<div style="font-size:13.5px;line-height:1.6;color:#d4d4d8;margin-bottom:10px;">'
                f'Compiled real-time technicals and quantitative fundamentals for <strong>{result["stock_name"]} ({result["ticker"]})</strong> from NSE.'
                f'<div style="margin-top:6px;color:#f4f4f5;">'
                f'<span style="font-family:\'JetBrains Mono\',monospace;font-size:10px;color:#a1a1aa;text-transform:uppercase;letter-spacing:0.06em;font-weight:700;">AI Synthesis: </span>'
                f'{synth_verdict}'
                f'</div>'
                f'</div>'
            )

            bot_response = f"{synth_html}{card_html}"

            st.session_state.risk_messages.append({
                "role": "bot",
                "content": bot_response
            })
        except FileNotFoundError:
            st.session_state.risk_messages.append({
                "role": "bot",
                "content": "⚠️ **Model Not Found**: Please ensure the risk model is trained using `python ml/train_model.py`."
            })
        except Exception as e:
            st.session_state.risk_messages.append({
                "role": "bot",
                "content": f"⚠️ **Analysis Unavailable**: Could not complete evaluation for '{target_symbol}'. ({str(e)})"
            })

    st.rerun()

# ─────────────────────────────────────────────
# CHAT TIMELINE RENDERING
# ─────────────────────────────────────────────
if not st.session_state.risk_messages:
    # Empty State — Conversational Copilot Welcome Card
    st.markdown("""
    <div class="ai-welcome-box">
        <div class="ai-welcome-icon">✦</div>
        <div class="ai-welcome-title">Welcome to Apex AI Financial Copilot</div>
        <div class="ai-welcome-desc">
            Your conversational investment analytics assistant. Ask about any Indian stock, or choose a prompt below to run institutional-grade machine learning risk evaluations, valuation health checks, and moving average tests.
        </div>
        <div class="ai-welcome-grid">
            <div class="ai-welcome-card">
                <div class="ai-welcome-card-title">💎 Bluechip Core</div>
                <div class="ai-welcome-card-sub">Reliance • TCS • HDFC Bank</div>
            </div>
            <div class="ai-welcome-card">
                <div class="ai-welcome-card-title">⚡ High Growth Tech</div>
                <div class="ai-welcome-card-sub">Infosys • Persistent • OFSS</div>
            </div>
            <div class="ai-welcome-card">
                <div class="ai-welcome-card-title">🛡 Defensive & FMCG</div>
                <div class="ai-welcome-card-sub">ITC • Sun Pharma • Britannia</div>
            </div>
            <div class="ai-welcome-card">
                <div class="ai-welcome-card-title">🚀 Momentum & Retail</div>
                <div class="ai-welcome-card-sub">Trent • Zomato • Titan</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Render Chat History
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.risk_messages:
        if msg["role"] == "user":
            user_html = (
                f'<div class="chat-row-user">'
                f'<div class="chat-bubble-user">'
                f'<div class="chat-sender-user">👤 You</div>'
                f'<div class="chat-content-user">{msg["content"]}</div>'
                f'</div>'
                f'</div>'
            )
            st.markdown(user_html, unsafe_allow_html=True)
        else:
            bot_html = (
                f'<div class="chat-row-bot">'
                f'<div class="chat-avatar-bot-sm">✦</div>'
                f'<div class="chat-bubble-bot">'
                f'<div class="chat-sender-bot">APEX AI COPILOT <span class="chat-sender-tag">ML SYNTHESIS</span></div>'
                f'{msg["content"]}'
                f'</div>'
                f'</div>'
            )
            st.markdown(bot_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown(
    '<p style="text-align:center;font-family:JetBrains Mono,monospace;font-size:0.70rem;'
    'color:#71717a;margin-top:2.5rem;letter-spacing:0.08em">'
    '© 2026 APEX STOCK SCREENER • AI RISK COPILOT • REAL-TIME QUANTITATIVE ENGINE</p>',
    unsafe_allow_html=True
)