import streamlit as st

def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <style>
        /* ===================================================== */
        /* ================= SIDEBAR BASE ====================== */
        /* ===================================================== */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #09090b 0%, #000000 100%) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            padding-top: 0px !important;
        }

        /* ── Remove Massive Empty Space at Top of Sidebar ── */
        [data-testid="stSidebarHeader"] {
            padding-top: 8px !important;
            padding-bottom: 0px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
            min-height: unset !important;
            height: auto !important;
        }

        [data-testid="stSidebarContent"] {
            padding-top: 0.5rem !important;
            padding-left: 14px !important;
            padding-right: 14px !important;
            padding-bottom: 1.5rem !important;
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

        /* ===================================================== */
        /* ============ BIG SIDEBAR TOGGLE BUTTON =============== */
        /* ===================================================== */
        button[kind="header"] {
            transform: scale(1.2);
            margin-left: 4px;
            margin-top: 4px;
            padding: 5px !important;
            border-radius: 50% !important;
            background: rgba(255, 255, 255, 0.04) !important;
            border: 1px solid rgba(255, 255, 255, 0.10) !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }

        button[kind="header"] svg {
            width: 26px !important;
            height: 26px !important;
            stroke: #ffffff !important;
            stroke-width: 2.2px !important;
            transition: all 0.3s ease;
        }

        button[kind="header"]:hover {
            background: rgba(255, 255, 255, 0.12) !important;
            border-color: rgba(255, 255, 255, 0.30) !important;
            box-shadow: 0 0 15px rgba(255, 255, 255, 0.25);
            transform: scale(1.48);
        }

        /* ===================================================== */
        /* ================= BRAND CARD ======================== */
        /* ===================================================== */
        .apex-brand-card {
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.015) 100%);
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 18px;
            padding: 18px 16px;
            margin-bottom: 20px;
            backdrop-filter: blur(14px);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .apex-brand-card:hover {
            border-color: rgba(255, 255, 255, 0.24);
            box-shadow: 0 12px 28px rgba(0, 0, 0, 0.6), 0 0 20px rgba(255, 255, 255, 0.04);
        }

        .apex-brand-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.35), transparent);
        }

        .apex-brand-title {
            font-family: 'Space Grotesk', -apple-system, sans-serif;
            font-size: 22px;
            font-weight: 800;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #ffffff 40%, #a1a1aa 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 4px;
        }

        .apex-brand-sub {
            font-family: 'DM Sans', -apple-system, sans-serif;
            font-size: 12px;
            color: #a1a1aa;
            line-height: 1.4;
            margin-bottom: 12px;
        }

        .apex-live-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 4px 10px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.16);
            font-family: 'JetBrains Mono', monospace;
            font-size: 10px;
            letter-spacing: 0.10em;
            color: #f4f4f5;
            text-transform: uppercase;
        }

        .apex-live-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: #ffffff;
            box-shadow: 0 0 8px rgba(255, 255, 255, 0.8);
            animation: pulseRadar 2s infinite ease-in-out;
        }

        /* ===================================================== */
        /* ============ SIDEBAR NAVIGATION LINKS =============== */
        /* ===================================================== */
        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"] {
            border-radius: 12px !important;
            margin-bottom: 4px !important;
            padding: 8px 12px !important;
            font-family: 'DM Sans', -apple-system, sans-serif !important;
            font-weight: 500 !important;
            color: #a1a1aa !important;
            transition: all 0.2s ease !important;
            border: 1px solid transparent !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"]:hover {
            background: rgba(255, 255, 255, 0.05) !important;
            color: #ffffff !important;
            border-color: rgba(255, 255, 255, 0.10) !important;
            transform: translateX(3px) !important;
        }

        section[data-testid="stSidebar"] [data-testid="stSidebarNavLink"][aria-current="page"] {
            background: rgba(255, 255, 255, 0.09) !important;
            color: #ffffff !important;
            border-color: rgba(255, 255, 255, 0.20) !important;
            font-weight: 600 !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
        }

        /* ===================================================== */
        /* ============ HIDE SIDEBAR SCROLLBAR (SLIDER) ======== */
        /* ===================================================== */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] * {
            scrollbar-width: none !important;
            -ms-overflow-style: none !important;
        }

        section[data-testid="stSidebar"]::-webkit-scrollbar,
        section[data-testid="stSidebar"] *::-webkit-scrollbar,
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"]::-webkit-scrollbar,
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"]::-webkit-scrollbar-thumb,
        section[data-testid="stSidebar"] div[data-testid="stSidebarContent"]::-webkit-scrollbar-track {
            display: none !important;
            width: 0px !important;
            height: 0px !important;
            background: transparent !important;
        }

        .user-status-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 12px 14px;
            margin-top: 24px;
            margin-bottom: 12px;
        }
        .user-status-email {
            font-family: 'JetBrains Mono', monospace;
            font-size: 11px;
            color: #f4f4f5;
            word-break: break-all;
        }
        .user-status-label {
            font-size: 10px;
            color: #71717a;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 2px;
        }

        /* Red Logout Button matching Settings Page */
        div.st-key-sidebar_logout_btn {
            margin-top: 6px !important;
        }
        div.st-key-sidebar_logout_btn button {
            background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%) !important;
            border: 1px solid rgba(239, 68, 68, 0.5) !important;
            color: #ffffff !important;
            font-family: 'DM Sans', -apple-system, sans-serif !important;
            font-weight: 700 !important;
            font-size: 13px !important;
            letter-spacing: 0.02em !important;
            border-radius: 12px !important;
            height: 40px !important;
            box-shadow: 0 4px 14px rgba(239, 68, 68, 0.25) !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div.st-key-sidebar_logout_btn button:hover {
            background: linear-gradient(90deg, #dc2626 0%, #b91c1c 100%) !important;
            box-shadow: 0 0 20px rgba(239, 68, 68, 0.55) !important;
            transform: translateY(-2px) !important;
            color: #ffffff !important;
        }
        div.st-key-sidebar_logout_btn button:active {
            transform: translateY(0) !important;
        }
        </style>

        <!-- BRAND CARD -->
        <div class="apex-brand-card">
            <div class="apex-brand-title">
                Apex Market
            </div>
            <div class="apex-brand-sub">
                FinTech Analytics & Screener
            </div>
            <div class="apex-live-pill">
                <span class="apex-live-dot"></span>
                System Live
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Show active user info if logged in
        user = st.session_state.get("user")
        if user and isinstance(user, dict):
            email = user.get("email", "Authenticated")
            st.markdown(f"""
            <div class="user-status-card">
                <div class="user-status-label">Active Session</div>
                <div class="user-status-email">● {email}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Logout", key="sidebar_logout_btn", use_container_width=True):
                st.session_state.logged_in = False
                st.session_state.user = None
                st.switch_page("合_Welcome.py")
