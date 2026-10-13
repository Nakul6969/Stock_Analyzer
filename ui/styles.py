import streamlit as st

def load_global_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=DM+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* =====================================================
       1. ROOT DESIGN TOKENS (OBSIDIAN & PLATINUM MONOCHROME)
       ===================================================== */
    :root {
      --bg-void: #000000;
      --bg-surface-1: #09090b;
      --bg-surface-2: #121214;
      --bg-surface-3: #18181b;

      --glass-bg: rgba(255, 255, 255, 0.035);
      --glass-bg-hover: rgba(255, 255, 255, 0.065);
      --glass-border: rgba(255, 255, 255, 0.10);
      --glass-border-hover: rgba(255, 255, 255, 0.28);
      --glass-border-glow: rgba(255, 255, 255, 0.45);

      --text-white: #ffffff;
      --text-silver: #f4f4f5;
      --text-muted: #a1a1aa;
      --text-dim: #71717a;

      --font-display: 'Space Grotesk', -apple-system, sans-serif;
      --font-body: 'DM Sans', -apple-system, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    /* =====================================================
       2. MASTER APP BACKGROUND & CANVAS
       ===================================================== */
    .stApp {
      background-color: var(--bg-void);
      background-image:
        radial-gradient(1000px 500px at 15% 10%, rgba(255, 255, 255, 0.035), transparent 70%),
        radial-gradient(800px 400px at 85% 15%, rgba(255, 255, 255, 0.025), transparent 70%),
        linear-gradient(180deg, #000000 0%, #070708 50%, #000000 100%);
      color: var(--text-silver);
      font-family: var(--font-body);
      min-height: 100vh;
      animation: fadeInSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Ambient Animated Subtle Tech Grid Overlay */
    .stApp::before {
      content: "";
      position: fixed;
      inset: 0;
      pointer-events: none;
      background-image:
        radial-gradient(1100px 600px at 50% 10%, rgba(255, 255, 255, 0.045) 0%, transparent 60%),
        linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
      background-size: 100% 100%, 48px 48px, 48px 48px;
      animation: gridDrift 24s linear infinite;
      z-index: 0;
    }

    @keyframes gridDrift {
      0% { background-position: 0 0, 0 0, 0 0; }
      50% { background-position: 0 0, 24px 24px, 24px 24px; }
      100% { background-position: 0 0, 48px 48px, 48px 48px; }
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stToolbar"] {
      background: transparent !important;
    }

    .block-container {
      padding-top: 1.2rem !important;
      padding-bottom: 2.5rem !important;
      max-width: 1240px;
    }

    /* =====================================================
       3. KEYFRAME ANIMATIONS
       ===================================================== */
    @keyframes fadeInSlideUp {
      from {
        opacity: 0;
        transform: translateY(10px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes tickerTape {
      0% { transform: translateX(0); }
      100% { transform: translateX(-50%); }
    }

    @keyframes pulseRadar {
      0% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7);
      }
      70% {
        transform: scale(1);
        box-shadow: 0 0 0 6px rgba(255, 255, 255, 0);
      }
      100% {
        transform: scale(0.95);
        box-shadow: 0 0 0 0 rgba(255, 255, 255, 0);
      }
    }

    @keyframes shimmer {
      0% { background-position: -200% 0; }
      100% { background-position: 200% 0; }
    }

    @keyframes borderBeamRotate {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    @keyframes floatSlow {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-4px); }
    }

    /* =====================================================
       4. TICKER TAPE / MARQUEE COMPONENT
       ===================================================== */
    .ticker-wrap {
      overflow: hidden;
      white-space: nowrap;
      background: rgba(255, 255, 255, 0.02);
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 10px 0;
      margin-bottom: 22px;
      position: relative;
    }

    .ticker-wrap::before, .ticker-wrap::after {
      content: "";
      position: absolute;
      top: 0;
      bottom: 0;
      width: 40px;
      z-index: 2;
      pointer-events: none;
    }
    .ticker-wrap::before {
      left: 0;
      background: linear-gradient(90deg, #000000, transparent);
    }
    .ticker-wrap::after {
      right: 0;
      background: linear-gradient(270deg, #000000, transparent);
    }

    .ticker-content {
      display: inline-block;
      animation: tickerTape 32s linear infinite;
    }

    .ticker-item {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-right: 38px;
      font-family: var(--font-mono);
      font-size: 13px;
      color: var(--text-silver);
    }

    .ticker-sym {
      color: var(--text-muted);
      font-weight: 500;
    }

    .ticker-val {
      color: var(--text-white);
      font-weight: 700;
    }

    .ticker-delta-up {
      color: #ffffff;
      background: rgba(255, 255, 255, 0.15);
      border: 1px solid rgba(255, 255, 255, 0.25);
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 700;
    }

    .ticker-delta-down {
      color: var(--text-muted);
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.10);
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }

    /* =====================================================
       5. BENTO GRID SYSTEM & LUXURY CARDS
       ===================================================== */
    .bento-card {
      background: linear-gradient(180deg, var(--glass-bg), rgba(255, 255, 255, 0.015));
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      padding: 24px 26px;
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      position: relative;
      overflow: hidden;
      margin-bottom: 18px;
    }

    .bento-card:hover {
      transform: translateY(-4px);
      border-color: var(--glass-border-hover);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 255, 255, 0.03);
    }

    .bento-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.25), transparent);
      opacity: 0.6;
    }

    /* Featured Beam Card */
    .bento-beam {
      position: relative;
      border: 1px solid var(--glass-border-glow);
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
      box-shadow: 0 0 30px rgba(255, 255, 255, 0.05);
    }

    .bento-beam::after {
      content: "";
      position: absolute;
      inset: -1px;
      border-radius: 20px;
      padding: 1px;
      background: linear-gradient(90deg, transparent 30%, rgba(255, 255, 255, 0.5) 50%, transparent 70%);
      -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
      -webkit-mask-composite: xor;
      mask-composite: exclude;
      animation: shimmer 4s infinite linear;
      background-size: 200% 100%;
    }

    /* Badge & Live Status */
    .live-badge {
      display: inline-flex;
      align-items: center;
      gap: 7px;
      padding: 5px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.16);
      font-family: var(--font-mono);
      font-size: 11px;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-white);
      margin-bottom: 12px;
    }

    .live-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #ffffff;
      display: inline-block;
      animation: pulseRadar 2s infinite ease-in-out;
    }

    /* Typography */
    h1, h2, h3, .heading-display {
      font-family: var(--font-display) !important;
      font-weight: 700 !important;
      letter-spacing: -0.02em !important;
      color: var(--text-white);
    }

    .gradient-text {
      background: linear-gradient(135deg, #ffffff 30%, #a1a1aa 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      display: inline-block;
    }

    .mono-value {
      font-family: var(--font-mono) !important;
      font-weight: 700;
      color: var(--text-white);
    }

    /* =====================================================
       6. BUTTONS & INPUT OVERRIDES
       ===================================================== */
    /* Target standard Streamlit CTA buttons without corrupting steppers/tabs */
    div[data-testid="stButton"] > button,
    div[data-testid="stFormSubmitButton"] > button,
    .stDownloadButton > button {
      border-radius: 14px !important;
      font-weight: 600 !important;
      letter-spacing: 0.02em !important;
      transition: all 0.25s ease !important;
      font-family: var(--font-body) !important;
    }

    div[data-testid="stButton"] > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover,
    .stDownloadButton > button:hover {
      transform: translateY(-2px) !important;
      box-shadow: 0 12px 24px rgba(0, 0, 0, 0.5) !important;
    }

    /* Primary High-Contrast Button */
    button[kind="primary"] {
      background: #ffffff !important;
      color: #000000 !important;
      border: 1px solid #ffffff !important;
      font-weight: 700 !important;
    }

    button[kind="primary"]:hover {
      background: #e4e4e7 !important;
      box-shadow: 0 0 25px rgba(255, 255, 255, 0.3) !important;
      transform: translateY(-2px) !important;
    }

    /* Secondary / Form Button */
    button[kind="secondary"] {
      background: rgba(255, 255, 255, 0.05) !important;
      color: #ffffff !important;
      border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }

    button[kind="secondary"]:hover {
      background: rgba(255, 255, 255, 0.10) !important;
      border-color: rgba(255, 255, 255, 0.35) !important;
    }

    /* Inputs */
    input, textarea, select {
      background: rgba(255, 255, 255, 0.04) !important;
      color: var(--text-white) !important;
      border-radius: 12px !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      font-family: var(--font-body) !important;
      transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    input:focus, textarea:focus, select:focus {
      border-color: rgba(255, 255, 255, 0.45) !important;
      box-shadow: 0 0 15px rgba(255, 255, 255, 0.10) !important;
      outline: none !important;
    }

    /* Number Input & Stepper Precision Fix - Clean Minimalist Input */
    div[data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"] {
      background: rgba(255, 255, 255, 0.04) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 12px !important;
      overflow: hidden !important;
      transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
      height: 44px !important;
      display: flex !important;
      align-items: center !important;
    }

    div[data-testid="stNumberInput"] div[data-testid="stNumberInputContainer"]:focus-within {
      border-color: rgba(255, 255, 255, 0.45) !important;
      box-shadow: 0 0 15px rgba(255, 255, 255, 0.12) !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      height: 100% !important;
      flex: 1 !important;
    }

    div[data-testid="stNumberInput"] input {
      background: transparent !important;
      border: none !important;
      box-shadow: none !important;
      color: #ffffff !important;
      font-family: var(--font-mono) !important;
      font-size: 15px !important;
      height: 100% !important;
      padding: 0 14px !important;
    }

    /* Eliminate the distorted floating stepper buttons */
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

    /* =====================================================
       SLIDER MONOCHROME ACCENT (PURE WHITE TRACK & THUMB)
       ===================================================== */
    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div {
      background: rgba(255, 255, 255, 0.14) !important;
      height: 6px !important;
      border-radius: 999px !important;
    }

    div[data-testid="stSlider"] [data-baseweb="slider"] > div > div > div,
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background: rgb"],
    div[data-testid="stSlider"] [data-baseweb="slider"] div[style*="background-color: rgb"] {
      background: #ffffff !important;
      background-color: #ffffff !important;
      height: 6px !important;
      border-radius: 999px !important;
      box-shadow: 0 0 10px rgba(255, 255, 255, 0.7), 0 0 2px rgba(255, 255, 255, 0.9) !important;
    }

    div[data-testid="stSlider"] div[role="slider"] {
      background-color: #ffffff !important;
      background: #ffffff !important;
      border: 2px solid #000000 !important;
      box-shadow: 0 0 14px rgba(255, 255, 255, 0.95), 0 2px 4px rgba(0, 0, 0, 0.6) !important;
      width: 18px !important;
      height: 18px !important;
      border-radius: 50% !important;
      transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }

    div[data-testid="stSlider"] div[role="slider"]:hover {
      transform: scale(1.15) !important;
      box-shadow: 0 0 18px rgba(255, 255, 255, 1.0) !important;
    }

    div[data-testid="stSlider"] div[role="slider"]:active {
      transform: scale(1.22) !important;
      box-shadow: 0 0 22px rgba(255, 255, 255, 1.0) !important;
    }

    div[data-testid="stSlider"] div[data-testid="stThumbValue"],
    div[data-testid="stSlider"] div[role="slider"] > div {
      color: #000000 !important;
      background: #ffffff !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-weight: 800 !important;
      font-size: 11px !important;
      border-radius: 6px !important;
      padding: 2px 6px !important;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }

    div[data-testid="stSlider"] [data-testid="stTickBarMin"],
    div[data-testid="stSlider"] [data-testid="stTickBarMax"],
    div[data-testid="stSlider"] [data-testid="stSliderTickBar"] {
      color: #71717a !important;
      font-family: 'JetBrains Mono', monospace !important;
      font-size: 11px !important;
      font-weight: 600 !important;
    }

    /* =====================================================
       TABS (DUAL-ENGINE: BASEWEB & STREAMLIT 1.65+ REACT ARIA)
       ===================================================== */
    div[data-testid="stTabs"],
    .stTabs {
      margin-top: 16px !important;
      margin-bottom: 20px !important;
    }

    div[data-testid="stTabs"] [role="tablist"],
    div[data-testid="stTabs"] [data-baseweb="tab-list"],
    .stTabs [role="tablist"],
    .stTabs [data-baseweb="tab-list"],
    [data-baseweb="tab-list"] {
      display: flex !important;
      width: 100% !important;
      gap: 8px !important;
      padding: 6px !important;
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.015) 100%) !important;
      border: 1px solid rgba(255, 255, 255, 0.12) !important;
      border-radius: 16px !important;
      backdrop-filter: blur(16px) !important;
      -webkit-backdrop-filter: blur(16px) !important;
      box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.06), 0 10px 30px rgba(0, 0, 0, 0.45) !important;
      overflow-x: auto !important;
      overflow-y: hidden !important;
    }

    /* Hide React Aria full-width bottom border pseudo-element on tablist */
    div[data-testid="stTabs"] [role="tablist"]::after,
    div[data-testid="stTabs"] [role="tablist"]::before,
    .stTabs [role="tablist"]::after,
    .stTabs [role="tablist"]::before {
      display: none !important;
      content: none !important;
      height: 0 !important;
      background: transparent !important;
    }

    div[data-testid="stTabs"] [role="tab"],
    div[data-testid="stTabs"] [data-testid="stTab"],
    div[data-testid="stTabs"] [data-baseweb="tab"],
    .stTabs [role="tab"],
    .stTabs [data-baseweb="tab"],
    [data-baseweb="tab"] {
      flex: 1 1 0% !important;
      display: flex !important;
      align-items: center !important;
      justify-content: center !important;
      text-align: center !important;
      height: auto !important;
      min-height: 44px !important;
      padding: 10px 20px !important;
      border-radius: 12px !important;
      color: var(--text-muted) !important;
      font-family: var(--font-display) !important;
      font-weight: 700 !important;
      font-size: 14px !important;
      letter-spacing: 0.02em !important;
      background: transparent !important;
      border: 1px solid transparent !important;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
      cursor: pointer !important;
      outline: none !important;
    }

    div[data-testid="stTabs"] [role="tab"] p,
    div[data-testid="stTabs"] [data-testid="stTab"] p,
    div[data-testid="stTabs"] [data-baseweb="tab"] p {
      margin: 0 !important;
      font-family: var(--font-display) !important;
      font-weight: 700 !important;
      font-size: 14px !important;
      letter-spacing: 0.02em !important;
      color: inherit !important;
    }

    div[data-testid="stTabs"] [role="tab"]:hover,
    div[data-testid="stTabs"] [data-testid="stTab"]:hover,
    div[data-testid="stTabs"] [data-testid="stTab"][data-hovered],
    div[data-testid="stTabs"] [data-baseweb="tab"]:hover,
    .stTabs [role="tab"]:hover,
    .stTabs [data-baseweb="tab"]:hover,
    [data-baseweb="tab"]:hover {
      color: #ffffff !important;
      background: rgba(255, 255, 255, 0.05) !important;
      border-color: rgba(255, 255, 255, 0.10) !important;
    }

    div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"],
    div[data-testid="stTabs"] [data-testid="stTab"][data-selected],
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"],
    .stTabs [role="tab"][aria-selected="true"],
    .stTabs [data-baseweb="tab"][aria-selected="true"],
    [data-baseweb="tab"][aria-selected="true"] {
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.14) 0%, rgba(255, 255, 255, 0.06) 100%) !important;
      color: #ffffff !important;
      border: 1px solid rgba(255, 255, 255, 0.28) !important;
      border-radius: 12px !important;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.22), 0 0 18px rgba(255, 255, 255, 0.06) !important;
    }

    /* Hide all default Streamlit / BaseWeb / React Aria underline bars and bottom borders */
    div[data-testid="stTabs"] .react-aria-SelectionIndicator,
    div[data-testid="stTabs"] [data-testid="stTab"] > span:not([data-testid="stMarkdownContainer"]),
    div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
    div[data-testid="stTabs"] [data-baseweb="tab-border"],
    div[data-testid="stTabs"] div[role="presentation"],
    .stTabs .react-aria-SelectionIndicator,
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"],
    [data-baseweb="tab-highlight"],
    [data-baseweb="tab-border"] {
      display: none !important;
      height: 0 !important;
      width: 0 !important;
      background: transparent !important;
      opacity: 0 !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.035), rgba(255, 255, 255, 0.015)) !important;
      border: 1px solid var(--glass-border) !important;
      border-radius: 16px !important;
      padding: 16px 20px !important;
      backdrop-filter: blur(10px) !important;
      transition: all 0.25s ease !important;
    }

    [data-testid="stMetric"]:hover {
      border-color: var(--glass-border-hover) !important;
      transform: translateY(-2px) !important;
    }

    [data-testid="stMetricLabel"] {
      font-family: var(--font-mono) !important;
      font-size: 11px !important;
      color: var(--text-muted) !important;
      letter-spacing: 0.08em !important;
      text-transform: uppercase !important;
    }

    [data-testid="stMetricValue"] {
      font-family: var(--font-mono) !important;
      font-size: 18px !important;
      font-weight: 700 !important;
      color: var(--text-white) !important;
      white-space: normal !important;
      word-break: break-word !important;
      overflow: visible !important;
      text-overflow: clip !important;
      line-height: 1.3 !important;
    }

    [data-testid="stMetricValue"] > div {
      white-space: normal !important;
      word-break: break-word !important;
      overflow: visible !important;
      text-overflow: clip !important;
    }

    /* Minimalist Platinum Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }

    ::-webkit-scrollbar-track {
      background: #000000;
    }

    ::-webkit-scrollbar-thumb {
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.28), rgba(255, 255, 255, 0.08));
      border-radius: 999px;
    }

    ::-webkit-scrollbar-thumb:hover {
      background: rgba(255, 255, 255, 0.45);
    }

    /* =====================================================
       DATA TABLES & DATAFRAMES (OBSIDIAN & PLATINUM)
       ===================================================== */
    div[data-testid="stDataFrame"],
    [data-testid="stDataFrame"] {
      background: #09090b !important;
      border: 1px solid rgba(255, 255, 255, 0.10) !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.45) !important;
    }

    div[data-testid="stDataFrame"] > div {
      background: #09090b !important;
      border-radius: 14px !important;
    }

    div[data-testid="stDataFrame"] iframe {
      background: #09090b !important;
      color-scheme: dark !important;
    }

    /* Streamlit Expander obsidian luxury styling */
    div[data-testid="stExpander"] {
      background: linear-gradient(180deg, rgba(255, 255, 255, 0.03) 0%, rgba(255, 255, 255, 0.01) 100%) !important;
      border: 1px solid rgba(255, 255, 255, 0.10) !important;
      border-radius: 14px !important;
      overflow: hidden !important;
      margin-bottom: 12px !important;
    }

    div[data-testid="stExpander"] summary {
      color: #ffffff !important;
      font-weight: 600 !important;
      padding: 12px 16px !important;
    }

    div[data-testid="stExpander"] summary:hover {
      background: rgba(255, 255, 255, 0.03) !important;
    }

    /* =====================================================
       SIDEBAR TOP GAP ELIMINATION & SCROLLBAR HIDING
       ===================================================== */
    section[data-testid="stSidebar"] {
      padding-top: 0px !important;
    }
    [data-testid="stSidebarHeader"] {
      padding-top: 8px !important;
      padding-bottom: 0px !important;
      min-height: unset !important;
      height: auto !important;
    }
    [data-testid="stSidebarContent"] {
      padding-top: 0.5rem !important;
    }
    [data-testid="stSidebarNav"] {
      padding-top: 0px !important;
      margin-top: 0px !important;
    }
    [data-testid="stSidebarNav"] > ul {
      padding-top: 0px !important;
      margin-top: 0px !important;
    }
    [data-testid="stSidebarNavSeparator"] {
      display: none !important;
    }
    [data-testid="stSidebarUserContent"] {
      padding-top: 0px !important;
      margin-top: 0px !important;
    }
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"] * {
      scrollbar-width: none !important;
      -ms-overflow-style: none !important;
    }
    section[data-testid="stSidebar"]::-webkit-scrollbar,
    section[data-testid="stSidebar"] *::-webkit-scrollbar {
      display: none !important;
      width: 0px !important;
      height: 0px !important;
    }

    /* Divider */
    hr {
      border: none;
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.12), transparent);
      margin: 28px 0;
    }

    /* Hide Streamlit default status widget (Running ... badges) */
    div[data-testid="stStatusWidget"],
    .stStatusWidget {
      visibility: hidden !important;
      display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
