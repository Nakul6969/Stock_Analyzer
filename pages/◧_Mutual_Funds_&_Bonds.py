import streamlit as st
import requests
import os
import pandas as pd
from dotenv import load_dotenv
import plotly.graph_objects as go
import plotly.express as px
from ui.sidebar import render_sidebar
from ui.styles import load_global_css

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Apex Mutual Fund Dashboard",
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

URL = "https://stock.indianapi.in/mutual_funds"
HEADERS = {"X-Api-Key": API_KEY}

if not API_KEY:
    st.error("API key not found")
    st.stop()

# ======================================================
# GLOBAL CSS (APEX THEME)
# ======================================================
st.markdown("""
<style>
/* Remove Form Border */
div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
    background: transparent !important;
    box-shadow: none !important;
}

.block-container { padding-top: 1rem; }

.page-title {
  font-size: 34px;
  font-weight: 900;
  background: linear-gradient(90deg, #ffffff, #a1a1aa);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: -0.02em;
}

/* ================= EQUAL-WIDTH LUXURY TABS ================= */
div[data-testid="stTabs"],
.stTabs {
  margin-top: 14px !important;
  margin-bottom: 16px !important;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"],
.stTabs [data-baseweb="tab-list"] {
  display: flex !important;
  width: 100% !important;
  gap: 8px !important;
  padding: 6px !important;
  background: rgba(255, 255, 255, 0.02) !important;
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  border-radius: 16px !important;
  backdrop-filter: blur(12px) !important;
}

div[data-testid="stTabs"] [data-baseweb="tab"],
.stTabs [data-baseweb="tab"] {
  flex: 1 1 0% !important;
  justify-content: center !important;
  text-align: center !important;
  padding: 11px 20px !important;
  font-size: 14px !important;
  font-weight: 700 !important;
  letter-spacing: 0.02em !important;
  color: #71717a !important;
  background: transparent !important;
  border-radius: 12px !important;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
  border: none !important;
}

div[data-testid="stTabs"] [data-baseweb="tab"]:hover,
.stTabs [data-baseweb="tab"]:hover {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.05) !important;
}

div[data-testid="stTabs"] [aria-selected="true"],
.stTabs [aria-selected="true"] {
  color: #ffffff !important;
  background: rgba(255, 255, 255, 0.10) !important;
  border: 1px solid rgba(255, 255, 255, 0.22) !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
}

div[data-testid="stTabs"] div[role="presentation"],
div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
div[data-testid="stTabs"] [data-baseweb="tab-border"],
div[data-testid="stTabs"] [aria-hidden="true"],
.stTabs div[role="presentation"],
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"],
.stTabs [aria-hidden="true"] {
  display: none !important;
  height: 0 !important;
}

/* ================= SIP LUXURY METRIC CARDS ================= */
.sip-card {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.015));
  border: 1px solid rgba(255, 255, 255, 0.10);
  border-radius: 16px;
  padding: 18px 20px;
  transition: all 0.25s ease;
  backdrop-filter: blur(14px);
  margin-bottom: 12px;
}

.sip-card:hover {
  border-color: rgba(255, 255, 255, 0.25);
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.45);
}

.sip-card-primary {
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.025));
  border: 1px solid rgba(255, 255, 255, 0.22);
  box-shadow: 0 0 25px rgba(255, 255, 255, 0.04);
}

.sip-card-label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #a1a1aa;
  margin-bottom: 8px;
}

.sip-card-val {
  font-family: 'Space Grotesk', 'JetBrains Mono', monospace;
  font-size: 24px;
  font-weight: 700;
  color: #ffffff;
  letter-spacing: -0.01em;
}

.sip-card-sub {
  font-size: 12px;
  color: #71717a;
  margin-top: 6px;
}

/* Benchmark pill tags */
.bench-pill {
  display: inline-block;
  background: rgba(255, 255, 255, 0.035);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 12px;
  color: #a1a1aa;
  margin-right: 6px;
  margin-bottom: 6px;
}

/* Eliminate distorted floating stepper buttons */
div[data-testid="stNumberInput"] button,
div[data-testid="stNumberInputStepDown"],
div[data-testid="stNumberInputStepUp"],
button[data-testid="stNumberInputStepDown"],
button[data-testid="stNumberInputStepUp"] {
  display: none !important;
  visibility: hidden !important;
  width: 0 !important;
  height: 0 !important;
  padding: 0 !important;
  margin: 0 !important;
  border: none !important;
}

/* SIP Input Field Explicit Header Labels */
.sip-input-label {
  font-family: 'DM Sans', -apple-system, sans-serif;
  font-size: 13px;
  font-weight: 700;
  color: #f4f4f5;
  letter-spacing: 0.02em;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 6px;
}
.sip-input-label-icon {
  font-size: 14px;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

st.markdown(
    '<div class="page-title">Apex Presents Mutual Fund & S.I.P Dashboard</div>',
    unsafe_allow_html=True
)
st.caption("One Stop Solution For Mutual Funds • SIP Calculation Smart Long-Term Investing")
st.caption("🎁 Top - 5 Funds In Every Category By Apex")
# ======================================================
# HELPERS
# ======================================================

def rupee(v):
    try:
        return f"₹ {float(v):,.2f}"
    except:
        return "—"

def percent(v):
    try:
        return f"{float(v):.2f}%"
    except:
        return "—"

def crore(v):
    try:
        return f"{float(v):,.0f} Cr"
    except:
        return "—"

def render_mf_table(funds):
    rows_html = ""
    for f in funds:
        fname = f.get("fund_name", "—")
        nav = rupee(f.get("latest_nav"))
        r1 = percent(f.get("1_year_return"))
        r3 = percent(f.get("3_year_return"))
        r5 = percent(f.get("5_year_return"))
        aum = crore(f.get("asset_size"))
        try:
            r_int = int(float(f.get("star_rating", 0)))
            rating_str = f'<span style="color:#f59e0b;letter-spacing:2px;">{"★" * r_int}{"☆" * (5 - r_int)}</span>'
        except:
            rating_str = '<span style="color:#71717a;">—</span>'

        rows_html += (
            f'<tr style="border-bottom:1px solid rgba(255,255,255,0.05);">'
            f'<td style="padding:12px 14px;color:#ffffff;font-weight:600;font-size:13.5px;max-width:320px;">{fname}</td>'
            f'<td style="padding:12px 14px;text-align:right;color:#f4f4f5;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;">{nav}</td>'
            f'<td style="padding:12px 14px;text-align:right;color:#22c55e;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;">{r1}</td>'
            f'<td style="padding:12px 14px;text-align:right;color:#22c55e;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;">{r3}</td>'
            f'<td style="padding:12px 14px;text-align:right;color:#22c55e;font-family:\'JetBrains Mono\',monospace;font-size:13px;font-weight:600;">{r5}</td>'
            f'<td style="padding:12px 14px;text-align:right;color:#d4d4d8;font-family:\'JetBrains Mono\',monospace;font-size:13px;">{aum}</td>'
            f'<td style="padding:12px 14px;text-align:center;font-size:13px;">{rating_str}</td>'
            f'</tr>'
        )

    return (
        f'<div style="background:linear-gradient(180deg, rgba(255,255,255,0.025) 0%, rgba(255,255,255,0.01) 100%);border:1px solid rgba(255,255,255,0.08);border-radius:14px;overflow-x:auto;box-shadow:0 6px 20px rgba(0,0,0,0.4);">'
        f'<table style="width:100%;border-collapse:collapse;text-align:left;font-family:\'DM Sans\',sans-serif;">'
        f'<thead>'
        f'<tr style="background:rgba(255,255,255,0.04);border-bottom:1px solid rgba(255,255,255,0.10);font-family:\'JetBrains Mono\',monospace;font-size:10px;font-weight:700;color:#a1a1aa;letter-spacing:0.08em;text-transform:uppercase;">'
        f'<th style="padding:11px 14px;">FUND NAME</th>'
        f'<th style="padding:11px 14px;text-align:right;">NAV</th>'
        f'<th style="padding:11px 14px;text-align:right;">1Y RETURN</th>'
        f'<th style="padding:11px 14px;text-align:right;">3Y RETURN</th>'
        f'<th style="padding:11px 14px;text-align:right;">5Y RETURN</th>'
        f'<th style="padding:11px 14px;text-align:right;">AUM</th>'
        f'<th style="padding:11px 14px;text-align:center;">RATING</th>'
        f'</tr>'
        f'</thead>'
        f'<tbody>'
        f'{rows_html}'
        f'</tbody>'
        f'</table>'
        f'</div>'
    )

# ======================================================
# FETCH MUTUAL FUND DATA
# ======================================================

@st.cache_data(ttl=300, show_spinner=False)
def fetch_mutual_funds():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    return r.json() if r.status_code == 200 else {}

data = fetch_mutual_funds()

# ======================================================
# MAIN TABS  (FIXED: removed extra comma)
# ======================================================

mf_tab, sip_tab = st.tabs(
    ["Mutual Funds", "✎ SIP Calculator"]
)

# ======================================================
# SIP CALCULATOR
# ======================================================

with sip_tab:
    st.markdown("""
    <div style="margin: 8px 0 20px 0;">
        <div style="font-size: 22px; font-weight: 800; color: #ffffff; letter-spacing: -0.02em;">
            Systematic Investment Plan (SIP) Calculator
        </div>
        <div style="font-size: 13px; color: #71717a; margin-top: 4px;">
            Simulate wealth accumulation and long-term capital compounding
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -------- INPUT CONTROLS --------
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown('<div class="sip-input-label"><span class="sip-input-label-icon">💰</span> Investment Amount (₹)</div>', unsafe_allow_html=True)
        sip_amount = st.number_input(
            "Investment Amount (₹)",
            min_value=500,
            max_value=1000000,
            value=10000,
            step=1000,
            label_visibility="collapsed",
            key="sip_amount_input",
            help="Monthly amount you plan to invest regularly"
        )

    with c2:
        st.markdown('<div class="sip-input-label"><span class="sip-input-label-icon">📈</span> Interest Rate (% p.a.)</div>', unsafe_allow_html=True)
        annual_return = st.number_input(
            "Interest Rate (% p.a.)",
            min_value=1.0,
            max_value=35.0,
            value=12.0,
            step=0.5,
            label_visibility="collapsed",
            key="sip_return_input",
            help="Anticipated compound annual growth rate (CAGR)"
        )

    with c3:
        st.markdown('<div class="sip-input-label"><span class="sip-input-label-icon">⏳</span> Time Period (Years)</div>', unsafe_allow_html=True)
        years = st.number_input(
            "Time Period (Years)",
            min_value=1,
            max_value=40,
            value=10,
            step=1,
            label_visibility="collapsed",
            key="sip_years_input",
            help="Total investment horizon in years"
        )

    # Benchmark Chips
    st.markdown("""
    <div style="margin: 10px 0 22px 0;">
        <span style="font-size: 11px; font-weight: 700; color: #71717a; text-transform: uppercase; letter-spacing: 0.08em; margin-right: 6px;">BENCHMARKS:</span>
        <span class="bench-pill">Nifty 50 Index ~12%</span>
        <span class="bench-pill">Flexi Cap Funds ~14%</span>
        <span class="bench-pill">Mid & Small Cap ~16%</span>
    </div>
    """, unsafe_allow_html=True)

    # -------- CALCULATIONS --------
    months = int(years * 12)
    monthly_rate = (annual_return / 100) / 12

    if monthly_rate > 0 and months > 0:
        future_value = sip_amount * (((1 + monthly_rate) ** months - 1) / monthly_rate) * (1 + monthly_rate)
    else:
        future_value = float(sip_amount * months)

    invested = float(sip_amount * months)
    gain = max(0.0, future_value - invested)
    roi_pct = (gain / invested * 100) if invested > 0 else 0.0

    def fmt_inr(v):
        if v >= 10000000:
            return f"₹ {v / 10000000:.2f} Cr"
        elif v >= 100000:
            return f"₹ {v / 100000:.2f} L"
        else:
            return f"₹ {v:,.0f}"

    # -------- LUXURY METRIC CARDS --------
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown(f"""
        <div class="sip-card">
            <div class="sip-card-label">TOTAL INVESTED</div>
            <div class="sip-card-val">₹ {invested:,.0f}</div>
            <div class="sip-card-sub">{months} deposits • {fmt_inr(invested)}</div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
        <div class="sip-card">
            <div class="sip-card-label">EST. WEALTH GAINED</div>
            <div class="sip-card-val" style="color: #ffffff; text-shadow: 0 0 14px rgba(255,255,255,0.25);">₹ {gain:,.0f}</div>
            <div class="sip-card-sub">+{roi_pct:.1f}% capital growth • {fmt_inr(gain)}</div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown(f"""
        <div class="sip-card sip-card-primary">
            <div class="sip-card-label" style="color: #ffffff;">TOTAL MATURITY CORPUS</div>
            <div class="sip-card-val" style="font-size: 26px; font-weight: 800; color: #ffffff;">₹ {future_value:,.0f}</div>
            <div class="sip-card-sub">{fmt_inr(future_value)} at {annual_return:.1f}% CAGR</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -------- VISUALIZATIONS ROW --------
    col_donut, col_traj = st.columns([1, 1.25])

    with col_donut:
        st.markdown(
            "<div style='font-size: 12px; font-weight: 700; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>Portfolio Asset Allocation</div>",
            unsafe_allow_html=True
        )

        fig_donut = go.Figure(data=[go.Pie(
            labels=["Invested Capital", "Est. Wealth Gain"],
            values=[invested, gain],
            hole=0.70,
            marker=dict(
                colors=["#27272a", "#ffffff"],
                line=dict(color="#09090b", width=2.5)
            ),
            textinfo="percent",
            textfont=dict(size=13, color=["#a1a1aa", "#000000"], family="Space Grotesk, sans-serif"),
            hovertemplate="<b>%{label}</b><br>Amount: ₹%{value:,.0f}<br>Share: %{percent}<extra></extra>",
            sort=False
        )])

        fig_donut.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.14,
                xanchor="center",
                x=0.5,
                font=dict(color="#a1a1aa", size=12, family="DM Sans, sans-serif")
            ),
            margin=dict(l=10, r=10, t=10, b=30),
            height=340,
            annotations=[
                dict(
                    text=f"<span style='font-size:10px;color:#71717a;letter-spacing:1.2px;font-family:JetBrains Mono;'>TOTAL CORPUS</span><br><b style='font-size:19px;color:#ffffff;font-family:Space Grotesk;'>{fmt_inr(future_value)}</b>",
                    x=0.5, y=0.5,
                    showarrow=False,
                    align="center"
                )
            ]
        )
        st.plotly_chart(fig_donut, use_container_width=True, config={"displayModeBar": False})

    with col_traj:
        st.markdown(
            "<div style='font-size: 12px; font-weight: 700; color: #a1a1aa; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;'>Compounding Growth Trajectory</div>",
            unsafe_allow_html=True
        )

        trajectory_data = []
        for y in range(1, int(years) + 1):
            m_y = y * 12
            fv_y = sip_amount * (((1 + monthly_rate) ** m_y - 1) / monthly_rate) * (1 + monthly_rate) if monthly_rate > 0 else float(sip_amount * m_y)
            inv_y = float(sip_amount * m_y)
            gain_y = max(0.0, fv_y - inv_y)
            trajectory_data.append({
                "Year": f"Yr {y}",
                "Invested": inv_y,
                "Gain": gain_y,
                "Total": fv_y
            })

        df_traj = pd.DataFrame(trajectory_data)

        fig_traj = go.Figure()
        fig_traj.add_trace(go.Bar(
            x=df_traj["Year"],
            y=df_traj["Invested"],
            name="Invested Capital",
            marker_color="#27272a",
            hovertemplate="Invested: ₹%{y:,.0f}<extra></extra>"
        ))
        fig_traj.add_trace(go.Bar(
            x=df_traj["Year"],
            y=df_traj["Gain"],
            name="Est. Wealth Gain",
            marker_color="#ffffff",
            hovertemplate="Gain: ₹%{y:,.0f}<extra></extra>"
        ))

        fig_traj.update_layout(
            barmode="stack",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=30),
            height=340,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.14,
                xanchor="center",
                x=0.5,
                font=dict(color="#a1a1aa", size=12, family="DM Sans, sans-serif")
            ),
            xaxis=dict(
                showgrid=False,
                color="#71717a",
                tickfont=dict(color="#a1a1aa", size=10, family="JetBrains Mono, monospace")
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="rgba(255,255,255,0.06)",
                color="#71717a",
                tickfont=dict(color="#a1a1aa", size=10, family="JetBrains Mono, monospace")
            ),
            hovermode="x unified"
        )
        st.plotly_chart(fig_traj, use_container_width=True, config={"displayModeBar": False})

    # Optional Year-by-Year schedule
    with st.expander("📊 View Year-by-Year Growth Schedule"):
        sched_rows_html = ""
        for r in trajectory_data:
            y = r.get("Year", "")
            inv = f"₹ {r.get('Invested', 0):,.0f}"
            gn = f"₹ {r.get('Gain', 0):,.0f}"
            tot = f"₹ {r.get('Total', 0):,.0f}"

            sched_rows_html += (
                f'<tr style="border-bottom:1px solid rgba(255,255,255,0.04);">'
                f'<td style="padding:10px 16px;font-family:\'JetBrains Mono\',monospace;font-size:12px;font-weight:700;color:#ffffff;">'
                f'<span style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);padding:2px 8px;border-radius:6px;">{y}</span>'
                f'</td>'
                f'<td style="padding:10px 16px;font-family:\'JetBrains Mono\',monospace;font-size:13px;color:#d4d4d8;text-align:right;">{inv}</td>'
                f'<td style="padding:10px 16px;font-family:\'JetBrains Mono\',monospace;font-size:13px;color:#22c55e;font-weight:600;text-align:right;">+{gn}</td>'
                f'<td style="padding:10px 16px;font-family:\'JetBrains Mono\',monospace;font-size:13px;color:#ffffff;font-weight:700;text-align:right;">{tot}</td>'
                f'</tr>'
            )

        sched_table_html = (
            f'<div style="background:linear-gradient(180deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.005) 100%);border:1px solid rgba(255,255,255,0.08);border-radius:12px;overflow-x:auto;box-shadow:0 4px 18px rgba(0,0,0,0.35);margin-top:4px;">'
            f'<table style="width:100%;border-collapse:collapse;font-family:\'DM Sans\',sans-serif;">'
            f'<thead>'
            f'<tr style="background:rgba(255,255,255,0.035);border-bottom:1px solid rgba(255,255,255,0.08);font-family:\'JetBrains Mono\',monospace;font-size:10px;font-weight:700;color:#a1a1aa;letter-spacing:0.08em;text-transform:uppercase;">'
            f'<th style="padding:11px 16px;text-align:left;">TIMELINE</th>'
            f'<th style="padding:11px 16px;text-align:right;">CUMULATIVE INVESTED</th>'
            f'<th style="padding:11px 16px;text-align:right;">ESTIMATED RETURNS</th>'
            f'<th style="padding:11px 16px;text-align:right;">TOTAL PORTFOLIO VALUE</th>'
            f'</tr>'
            f'</thead>'
            f'<tbody>'
            f'{sched_rows_html}'
            f'</tbody>'
            f'</table>'
            f'</div>'
        )
        st.markdown(sched_table_html, unsafe_allow_html=True)


# ======================================================
# MUTUAL FUND DATA
# ======================================================

with mf_tab:
    if not data:
        st.warning("No mutual fund data available")
    else:
        tabs = st.tabs(list(data.keys()))
        for tab, category in zip(tabs, data.keys()):
            with tab:
                for subcat, funds in data[category].items():
                    with st.expander(f"📁 {subcat} • {len(funds)} funds"):
                        if not funds:
                            st.info("No funds available")
                            continue

                        st.markdown(render_mf_table(funds), unsafe_allow_html=True)

# ======================================================
# FOOTER
# ======================================================
st.divider()
st.caption("© 2025 Apex Stock Screener • Mutual Funds • SIP • SWP • Built with Streamlit")

