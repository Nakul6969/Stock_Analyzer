import streamlit as st

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="Account Settings · Apex",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from ui.styles import load_global_css
from ui.sidebar import render_sidebar
from auth.auth import render_auth
from auth.auth_utils import verify_password, hash_password
from database.db import users_col
from dotenv import load_dotenv
import os
import re
import smtplib
import random
import time
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# ---------------- LOAD LOGO ----------------
def get_logo_b64():
    try:
        with open("assets/logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

logo_b64 = get_logo_b64()

# ---------------- CSS ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* ════════ HERO BANNER ════════ */
.hero-banner {
    position: relative;
    background: linear-gradient(135deg, #121212 0%, #1a1a1a 40%, #080808 100%);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 0;
    margin-bottom: 2rem;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -40px; left: 20%;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(255,255,255,0.04) 0%, transparent 65%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-inner {
    display: flex;
    align-items: center;
    gap: 1.6rem;
    padding: 1.8rem 2.2rem;
    position: relative;
    z-index: 1;
}
.hero-avatar {
    width: 68px; height: 68px;
    border-radius: 50%;
    border: 2px solid rgba(255,255,255,0.25);
    box-shadow: 0 0 24px rgba(255,255,255,0.12);
    overflow: hidden;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255,255,255,0.05);
}
.hero-avatar img { width:100%;height:100%;object-fit:cover; }
.hero-avatar-fallback {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    color: #ffffff;
}
.hero-text { flex: 1; }
.hero-greeting {
    font-family: 'DM Serif Display', serif;
    font-size: 1.7rem;
    color: #ffffff;
    margin: 0 0 0.2rem;
    letter-spacing: -0.01em;
    line-height: 1.2;
}
.hero-greeting span { color: #ffffff; }
.hero-sub {
    font-size: 0.82rem;
    color: #8e8e93;
    margin: 0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.04em;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 4px 12px;
    margin-top: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: #ffffff;
    letter-spacing: 0.08em;
}
.hero-badge::before {
    content: '';
    width: 5px; height: 5px;
    background: #22c55e;
    border-radius: 50%;
    animation: pulse-dot 2s infinite;
}
@keyframes pulse-dot { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.5;transform:scale(0.8)} }

/* ════════ SECTION CARDS ════════ */
.s-card {
    background: #111111;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 1.4rem;
    transition: border-color 0.2s;
}
.s-card:hover { border-color: rgba(255,255,255,0.12); }
.s-card-header {
    padding: 1.2rem 1.6rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.042);
    display: flex;
    align-items: center;
    gap: 10px;
}
.s-card-icon {
    width: 32px; height: 32px;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.10);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.9rem;
    flex-shrink: 0;
}
.s-card-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1rem;
    color: #cce9ff;
    margin: 0;
}
.s-card-desc {
    font-size: 0.75rem;
    color: #737373;
    margin: 1px 0 0;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.03em;
}
.s-card-body { padding: 1.4rem 1.6rem; }

/* ════════ INFO FIELDS ════════ */
.info-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}
.info-field {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 0.85rem 1.1rem;
    position: relative;
}
.info-field-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.65rem;
    color: #737373;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 0.4rem;
}
.info-field-value {
    font-size: 0.92rem;
    color: #f5f5f5;
    font-weight: 500;
    word-break: break-all;
}
.info-field-badge {
    position: absolute;
    top: 0.6rem; right: 0.8rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    background: rgba(255,255,255,0.05);
    color: #ffffff;
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 2px 8px;
    letter-spacing: 0.06em;
}

/* ════════ OTP STEPS ════════ */
.step-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 1rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: #737373;
}
.step-dot {
    width: 22px; height: 22px;
    border-radius: 50%;
    border: 1.5px solid rgba(255,255,255,0.15);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.6rem;
    color: #737373;
    flex-shrink: 0;
}
.step-dot.active {
    background: rgba(255,255,255,0.08);
    border-color: #ffffff;
    color: #ffffff;
}
.step-dot.done {
    background: rgba(34,197,94,0.12);
    border-color: #22c55e;
    color: #22c55e;
}
.step-line {
    flex: 1;
    height: 1px;
    background: rgba(255,255,255,0.05);
}

/* ════════ INPUT OVERRIDES ════════ */
div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] [data-baseweb="base-input"],
div[data-testid="stTextInput"] [data-baseweb="input"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #f5f5f5 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.94rem !important;
    padding-right: 3rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #737373 !important; }
div[data-testid="stTextInput"] input:focus {
    border-color: rgba(255,255,255,0.25) !important;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.042) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] label {
    color: #8e8e93 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase !important;
}
div[data-testid="stTextInput"] button {
    background: transparent !important;
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    padding: 0 0.5rem !important;
}
div[data-testid="stTextInput"] button:hover,
div[data-testid="stTextInput"] button:focus,
div[data-testid="stTextInput"] button:focus-visible {
    background: transparent !important;
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}
div[data-testid="stTextInput"] button svg { fill:#3d6b8a !important;stroke:#3d6b8a !important; }
div[data-testid="stTextInput"] button:hover svg { fill:#ffffff !important;stroke:#ffffff !important; }

/* ════════ BUTTON OVERRIDES ════════ */
div[data-testid="stButton"] > button {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    height: 44px !important;
    transition: all 0.2s !important;
    letter-spacing: 0.02em !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]) {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e5e7eb !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]):hover {
    background: rgba(255,255,255,0.10) !important;
    border-color: rgba(255,255,255,0.30) !important;
    transform: translateY(-1px) !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(90deg, #ef4444, #dc2626) !important;
    border: none !important;
    color: #fff !important;
    font-weight: 700 !important;
    border-radius: 10px !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #dc2626, #b91c1c) !important;
    box-shadow: 0 0 18px rgba(239,68,68,0.30) !important;
    transform: translateY(-1px) !important;
}

/* ════════ SIGN OUT CARD ════════ */
.signout-inner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1.2rem 1.6rem;
}
.signout-text p { margin: 0; }
.signout-label { font-size: 0.88rem; color: #8e8e93; }
.signout-warn {
    font-size: 0.75rem;
    color: #737373;
    font-family: 'JetBrains Mono', monospace;
    margin-top: 3px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- AUTH GUARD ----------------
if not st.session_state.get("logged_in"):
    render_auth()
    st.stop()

# ---------------- USER DATA FETCHING ----------------
@st.cache_data(ttl=60, show_spinner=False)
def fetch_user(email):
    if not email:
        return {}
    try:
        user = users_col.find_one({"email": email}, {"_id": 0, "userid": 1, "email": 1, "password": 1})
        return user if user else {}
    except Exception:
        return {}

# ---------------- USER DATA ----------------
session_email = st.session_state.get("user", {}).get("email", "")
user_data     = fetch_user(session_email)
user_name     = user_data.get("userid", st.session_state.get("user", {}).get("userid", "User"))
user_email    = user_data.get("email",  st.session_state.get("user", {}).get("email", ""))

load_global_css()
render_sidebar()

# ════════════════════════════════════════
#  HERO BANNER
# ════════════════════════════════════════
avatar_html = (
    f'<img src="data:image/png;base64,{logo_b64}" alt="logo">'
    if logo_b64 else
    f'<span class="hero-avatar-fallback">{user_name[0].upper() if user_name else "A"}</span>'
)

initials = (user_name[0].upper() if user_name else "A")

st.markdown(f"""
<div class="hero-banner">
    <div class="hero-inner">
        <div class="hero-avatar">{avatar_html}</div>
        <div class="hero-text">
            <p class="hero-greeting">Hello, <span>{user_name}</span> 👋</p>
            <p class="hero-sub">account settings · apex stock screener</p>
            <div class="hero-badge">ACTIVE SESSION</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════
#  PROFILE CARD
# ════════════════════════════════════════
st.markdown("""
<div class="s-card">
    <div class="s-card-header">
        <div class="s-card-icon">👤</div>
        <div>
            <p class="s-card-title">Your Profile</p>
            <p class="s-card-desc">READ-ONLY · CANNOT BE MODIFIED</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="s-card-body">
    <div class="info-grid">
        <div class="info-field">
            <div class="info-field-label">User ID</div>
            <div class="info-field-value">{user_name}</div>
            <span class="info-field-badge">locked</span>
        </div>
        <div class="info-field">
            <div class="info-field-label">Email Address</div>
            <div class="info-field-value">{user_email}</div>
            <span class="info-field-badge">locked</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════
#  OTP HELPER
# ════════════════════════════════════════
def send_otp_email(to_email, otp):
    try:
        try:
            EMAIL_USER = st.secrets["EMAIL_USER"]
            EMAIL_PASS = st.secrets["EMAIL_PASS"]
        except Exception:
            EMAIL_USER = os.getenv("EMAIL_USER")
            EMAIL_PASS = os.getenv("EMAIL_PASS")

        if not EMAIL_USER or not EMAIL_PASS:
            st.error("❌ Email credentials missing.")
            return False

        msg            = MIMEMultipart("alternative")
        msg["Subject"] = "Apex Screener — Your OTP Code"
        msg["From"]    = EMAIL_USER
        msg["To"]      = to_email

        html = f"""
        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; background-color: #030712; margin: 0; padding: 0;">
            <tr>
                <td align="center" style="padding: 40px 10px;">
                    <table border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 480px; background-color: #0b1329; border: 1px solid rgba(255, 255, 255, 0.120); border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
                        <!-- Header -->
                        <tr>
                            <td style="padding: 32px 32px 20px 32px; border-bottom: 1px solid rgba(255, 255, 255, 0.060);">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                    <tr>
                                        <td width="48" style="padding-right: 12px; vertical-align: middle;">
                                            <div style="width: 40px; height: 40px; border-radius: 50%; background-color: rgba(255, 255, 255, 0.060); border: 1px solid rgba(255, 255, 255, 0.180); text-align: center; line-height: 40px; font-size: 20px;">🔐</div>
                                        </td>
                                        <td style="vertical-align: middle;">
                                            <div style="font-size: 18px; font-weight: 700; color: #f3f4f6; letter-spacing: 0.5px;">Apex Stock Screener</div>
                                            <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">Password Change Request</div>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <!-- Body -->
                        <tr>
                            <td style="padding: 32px;">
                                <p style="font-size: 15px; line-height: 24px; color: #d1d5db; margin: 0 0 20px 0;">
                                    Hello,
                                </p>
                                <p style="font-size: 15px; line-height: 24px; color: #d1d5db; margin: 0 0 24px 0;">
                                    We received a request to change your password for your Apex Stock Screener account. Use the one-time password (OTP) below to complete the verification:
                                </p>
                                
                                <!-- OTP Box -->
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="margin-bottom: 24px;">
                                    <tr>
                                        <td align="center" style="background-color: rgba(255, 255, 255, 0.030); border: 1px solid rgba(255, 255, 255, 0.120); border-radius: 12px; padding: 24px;">
                                            <span style="font-family: 'Courier New', Courier, monospace; font-size: 38px; font-weight: 800; letter-spacing: 8px; color: #ffffff; white-space: nowrap; word-break: keep-all; display: inline-block; padding-left: 8px;">{otp}</span>
                                        </td>
                                    </tr>
                                </table>

                                <p style="font-size: 13px; line-height: 20px; color: #9ca3af; margin: 0 0 24px 0;">
                                    This OTP is valid for <strong style="color: #f3f4f6;">5 minutes</strong>. For security reasons, please do not share this code with anyone.
                                </p>
                                <p style="font-size: 13px; line-height: 20px; color: #6b7280; margin: 0; border-top: 1px solid rgba(255, 255, 255, 0.060); padding-top: 20px;">
                                    If you did not request this change, you can safely ignore this email. Your password will remain unchanged.
                                </p>
                            </td>
                        </tr>
                        <!-- Footer -->
                        <tr>
                            <td style="background-color: #070d19; padding: 20px 32px; text-align: center; font-size: 11px; color: #4b5563;">
                                &copy; 2026 Apex Stock Screener &bull; FinTech Analytics Platform
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
        </table>
        """
        msg.attach(MIMEText(html, "html"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo(); server.starttls(); server.ehlo()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"❌ Failed to send OTP: {e}")
        return False

# ════════════════════════════════════════
#  OTP SESSION INIT
# ════════════════════════════════════════
for k, v in [("otp_code", None), ("otp_expiry", None), ("otp_verified", False), ("otp_sent", False)]:
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════════
#  PASSWORD CARD
# ════════════════════════════════════════
step1_class = "done" if st.session_state.otp_sent    else "active"
step2_class = "done" if st.session_state.otp_verified else ("active" if st.session_state.otp_sent else "")
step3_class = "active" if st.session_state.otp_verified else ""

st.markdown(f"""
<div class="s-card">
    <div class="s-card-header">
        <div class="s-card-icon">🔐</div>
        <div>
            <p class="s-card-title">Change Password</p>
            <p class="s-card-desc">OTP VERIFICATION · EMAIL PROTECTED</p>
        </div>
    </div>
    <div class="s-card-body">
        <div class="step-indicator">
            <div class="step-dot {step1_class}">1</div>
            <span>Send OTP</span>
            <div class="step-line"></div>
            <div class="step-dot {step2_class}">2</div>
            <span>Verify</span>
            <div class="step-line"></div>
            <div class="step-dot {step3_class}">3</div>
            <span>New Password</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# STEP 1 — Send OTP
if not st.session_state.otp_verified:
    with st.container():
        st.markdown('<div style="padding:0 1.6rem 1.4rem">', unsafe_allow_html=True)

        col1, col_btn, col3 = st.columns([1, 1, 1])
        with col_btn:
            send_clicked = st.button(
                "📧 Send OTP" if not st.session_state.otp_sent else "🔁 Resend OTP",
                use_container_width=True,
                key="send_otp_btn"
            )

        if send_clicked:
            otp = str(random.randint(100000, 999999))
            st.session_state.otp_code   = otp
            st.session_state.otp_expiry = time.time() + 300
            st.session_state.otp_sent   = True
            if send_otp_email(user_email, otp):
                st.success(f"✅ OTP sent to **{user_email}**")

        # STEP 2 — Verify OTP
        if st.session_state.otp_sent:
            st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
            otp_input = st.text_input(
                "Enter OTP",
                placeholder="_ _ _ _ _ _",
                max_chars=6,
                key="otp_input"
            )
            col1, col_btn2, col3 = st.columns([1, 1, 1])
            with col_btn2:
                verify_clicked = st.button("✅ Verify OTP", use_container_width=True, key="verify_btn")

            if verify_clicked:
                if not otp_input:
                    st.warning("⚠️ Please enter the OTP.")
                elif time.time() > st.session_state.otp_expiry:
                    st.error("❌ OTP expired. Request a new one.")
                    st.session_state.otp_sent = False
                    st.session_state.otp_code = None
                elif otp_input.strip() == st.session_state.otp_code:
                    st.session_state.otp_verified = True
                    st.success("✅ OTP verified!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect OTP.")

        st.markdown('</div>', unsafe_allow_html=True)

# STEP 3 — New Password
else:
    with st.container():
        st.markdown('<div style="padding:0 1.6rem 1.4rem">', unsafe_allow_html=True)
        st.info("🔓 Identity verified. Set your new password below.")

        new_pass     = st.text_input("New Password",         type="password", key="new_pass",     placeholder="Minimum 4 characters")
        confirm_pass = st.text_input("Confirm New Password", type="password", key="confirm_pass", placeholder="Re-enter new password")

        col1, col_btn3, col3 = st.columns([1, 1, 1])
        with col_btn3:
            update_clicked = st.button("Update Password", use_container_width=True, key="update_btn")

        if update_clicked:
            if not new_pass or not confirm_pass:
                st.warning("⚠️ Please fill in both fields.")
            elif len(new_pass) < 4:
                st.warning("⚠️ Password must be at least 4 characters.")
            elif new_pass != confirm_pass:
                st.error("❌ Passwords do not match.")
            else:
                try:
                    try:
                        uri = st.secrets["MONGO_URI"]
                    except Exception:
                        uri = os.getenv("MONGO_URI")
                    client = MongoClient(uri)
                    col    = client["apex_auth"]["users"]
                    col.update_one(
                        {"email": session_email},
                        {"$set": {"password": hash_password(new_pass)}}
                    )
                    for k in ["otp_code", "otp_expiry", "otp_verified", "otp_sent"]:
                        st.session_state[k] = None if k in ["otp_code","otp_expiry"] else False
                    fetch_user.clear()
                    st.success("✅ Password updated successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to update: {e}")

        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ════════════════════════════════════════
#  SIGN OUT CARD
# ════════════════════════════════════════
st.markdown("""
<div class="s-card">
    <div class="signout-inner">
        <div class="signout-text">
            <p class="s-card-title" style="font-family:'DM Serif Display',serif;font-size:1rem;color:#cce9ff;margin:0 0 3px">🚪 Sign Out</p>
            <p class="signout-warn">SESSION WILL BE TERMINATED · REDIRECTED TO LOGIN</p>
        </div>
""", unsafe_allow_html=True)

col1, col_lg, col3 = st.columns([1, 1, 1])
with col_lg:
    if st.button("Logout", use_container_width=True, type="primary", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown("</div></div>", unsafe_allow_html=True)

# ════════════════════════════════════════
#  FOOTER
# ════════════════════════════════════════
st.markdown(
    '<p style="text-align:center;font-family:JetBrains Mono,monospace;'
    'font-size:0.65rem;color:#0f2333;margin-top:1.5rem;letter-spacing:0.1em">'
    '© 2026 APEX STOCK SCREENER · ACCOUNT SETTINGS</p>',
    unsafe_allow_html=True
)