import streamlit as st
import re
from database.db import users_col, check_db_health
from auth.auth_utils import hash_password, verify_password
from datetime import datetime
import base64
import requests
from urllib.parse import urlencode
import smtplib
import random
import time
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@st.cache_data(show_spinner=False)
def img_to_base64(path: str) -> str:
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return ""


logo_base64 = img_to_base64("assets/logo.png")


def send_forgot_otp_email(to_email, otp):
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
        msg["Subject"] = "Apex Screener — Password Reset OTP"
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
                                            <div style="width: 40px; height: 40px; border-radius: 50%; background-color: rgba(255, 255, 255, 0.060); border: 1px solid rgba(255, 255, 255, 0.180); text-align: center; line-height: 40px; font-size: 20px;">🔑</div>
                                        </td>
                                        <td style="vertical-align: middle;">
                                            <div style="font-size: 18px; font-weight: 700; color: #f3f4f6; letter-spacing: 0.5px;">Apex Stock Screener</div>
                                            <div style="font-size: 12px; color: #9ca3af; margin-top: 2px;">Forgot Password Verification</div>
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
                                    We received a request to reset the password for your Apex Stock Screener account. Use the one-time password (OTP) below to complete the verification:
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

# Google Heplper Function-------------------------------------------

def get_google_auth_url():
    try:
        client_id    = str(st.secrets["google_oauth"]["client_id"]).strip()
        redirect_uri = str(st.secrets["google_oauth"]["redirect_uri"]).strip().rstrip("/")
    except Exception:
        return None
    params = {
        "client_id":     client_id,
        "redirect_uri":  redirect_uri,
        "response_type": "code",
        "scope":         "openid email profile",
        "access_type":   "offline",
        "prompt":        "select_account",
    }
    return "https://accounts.google.com/o/oauth2/v2/auth?" + urlencode(params)


def exchange_code_for_token(code):
    try:
        client_id     = str(st.secrets["google_oauth"]["client_id"]).strip()
        client_secret = str(st.secrets["google_oauth"]["client_secret"]).strip()
        redirect_uri  = str(st.secrets["google_oauth"]["redirect_uri"]).strip().rstrip("/")
    except Exception:
        return None
    resp = requests.post("https://oauth2.googleapis.com/token", data={
        "code":          code,
        "client_id":     client_id,
        "client_secret": client_secret,
        "redirect_uri":  redirect_uri,
        "grant_type":    "authorization_code",
    })
    return resp.json() if resp.status_code == 200 else None


def get_google_user_info(access_token):
    resp = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    return resp.json() if resp.status_code == 200 else None


def handle_google_callback():
    code = st.query_params.get("code")
    if not code:
        return False

    try:
        token_data = exchange_code_for_token(code)
        if not token_data or "access_token" not in token_data:
            st.error("❌ Google login failed. Please try again.")
            st.query_params.clear()
            return False

        user_info = get_google_user_info(token_data["access_token"])
        if not user_info:
            st.error("❌ Could not fetch Google account info.")
            st.query_params.clear()
            return False

        email     = user_info.get("email", "").strip().lower()
        name      = user_info.get("name", email.split("@")[0])
        google_id = user_info.get("id", "")

        try:
            existing = users_col.find_one({"email": {"$regex": f"^{re.escape(email)}$", "$options": "i"}})

            if not existing:
                users_col.insert_one({
                    "email":         email,
                    "userid":        name,
                    "password":      None,
                    "auth_provider": "google",
                    "google_id":     google_id,
                    "created_at":    datetime.utcnow()
                })
                existing = users_col.find_one({"email": email})

            st.session_state.logged_in = True
            st.session_state.user = {
                "email":         existing["email"],
                "userid":        existing["userid"],
                "auth_provider": existing.get("auth_provider", "google")
            }
            st.query_params.clear()
            st.rerun()
            return True
        except Exception as e:
            st.error(f"❌ Database error: Could not reach MongoDB Atlas. Please ensure IP access is allowed in MongoDB Atlas Network Access (allow 0.0.0.0/0).")
            st.query_params.clear()
            return False
    except Exception as e:
        st.error(f"❌ Google OAuth error: {e}")
        st.query_params.clear()
        return False


def _render_google_button():
    auth_url = get_google_auth_url()
    if not auth_url:
        auth_url = "?error=google_not_configured"
    st.markdown(f"""
    <a href="{auth_url}" target="_self" style="text-decoration:none; display:block; width:100%;">
        <div class="google-btn">
            <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" height="18">
            <span>Continue with Google</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

# PAGE CONFIG (only when running this file directly)
if __name__ == "__main__":
    st.set_page_config(
        page_title="Apex - Auth",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

# SESSION INIT

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# LOGIN VIEW

def login_view():
    st.markdown(f"""
    <div class="auth-logo">
        <img src="data:image/png;base64,{logo_base64}">
    </div>

    <div class="auth-title">Apex Analyzer Login</div>
    <div class="auth-subtitle">
        Next-Gen Intelligence & Secure Access To Stock Information
    </div>
    """, unsafe_allow_html=True)

    # -------- LOGIN FORM --------
    with st.form("login_form"):
        userid = st.text_input("UserID", placeholder="Enter userID...")
        password = st.text_input(
            "Password",
            placeholder="Enter password...",
            type="password"
        )
        submit = st.form_submit_button("Login", key="l_btn", use_container_width=True)

    # -------- LOGIN LOGIC --------
    if submit:
        if not userid or not password:
            st.error("Please fill in all fields ❌")
            return

        # Normalize userid: trim spaces and match case-insensitively
        userid_norm = (userid or "").strip()
        try:
            user = users_col.find_one({
                "userid": {"$regex": f"^{re.escape(userid_norm)}$", "$options": "i"}
            })
        except Exception as e:
            st.error(f"⚠️ Database connection error: Could not reach MongoDB Atlas. Please ensure your IP address is whitelisted in MongoDB Atlas Network Access.")
            return

        if not user:
            st.error("User Not Found ❌ - If You Are New Please Sign Up")
            return

        if not user.get("password"):
            st.error("This account uses Google login ❌")
            return

        if verify_password(password, user["password"]):
            st.session_state.logged_in = True
            st.session_state.user = {
                "email": user["email"],
                "userid": user["userid"],
                "auth_provider": user["auth_provider"]
            }
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid password ❌")

    # -------- FORGOT PASSWORD LINK --------
    st.markdown("""
    <div style="text-align: center; margin-top: 15px;">
        <a href="?action=forgot_password" target="_self" style="color: #ffffff; text-decoration: underline; font-weight: 600; font-size: 14px;">Forgot Password?</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div style="text-align:center; margin:16px 0; color:#9ca3af; font-size:13px;">or</div>',
        unsafe_allow_html=True
    )

    _render_google_button()

# =========================================================
# SIGNUP VIEW
# =========================================================
def signup_view():
    st.markdown(f"""
    <div class="auth-logo">
        <img src="data:image/png;base64,{logo_base64}">
    </div>

    <div class="auth-title">Create Apex Account</div>
    <div class="auth-subtitle">
        Join the future of intelligent stock analytics
    </div>
    """, unsafe_allow_html=True)

    # -------- SIGNUP FORM (ONLY ONCE) --------
    with st.form("signup_form"):
        email = st.text_input("Email ID", placeholder="Enter email address...")
        userid = st.text_input("UserID", placeholder="Enter your name...")
        password = st.text_input(
            "Create Password",
            placeholder="Minimum 4 characters...",
            type="password"
        )

        submit = st.form_submit_button("Sign Up", key="btn_s", use_container_width=True)

    # -------- SIGNUP LOGIC --------
    if submit:
        if not email or not userid or not password:
            st.error("All fields are required ❌")
            return

        if len(password) < 4:
            st.error("Password must be at least 4 characters ❌")
            return

        # Normalize inputs
        email_norm = (email or "").strip()
        userid_norm = (userid or "").strip()

        # Case-insensitive duplicate check on trimmed values
        try:
            exists = users_col.find_one({
                "$or": [
                    {"email": {"$regex": f"^{re.escape(email_norm)}$", "$options": "i"}},
                    {"userid": {"$regex": f"^{re.escape(userid_norm)}$", "$options": "i"}},
                ]
            })
        except Exception as e:
            st.error("⚠️ Database connection error: Could not reach MongoDB Atlas. Please ensure your IP address is whitelisted in MongoDB Atlas Network Access.")
            return

        if exists:
            st.error("User already exists ❌")
            return

        try:
            users_col.insert_one({
                "email": email_norm,
                "userid": userid_norm,
                "password": hash_password(password),
                "auth_provider": "local",
                "created_at": datetime.utcnow()
            })
            st.success("Account created successfully ✅ Please login")
            st.session_state.auth_tab = "login"
            st.rerun()
        except Exception as e:
            st.error(f"⚠️ Failed to save user: {e}")
            return

    st.markdown(
        '<div style="text-align:center; margin:16px 0; color:#9ca3af; font-size:13px;">or</div>',
        unsafe_allow_html=True
    )

    _render_google_button()


def forgot_password_view():
    step1_class = "done" if st.session_state.forgot_otp_sent    else "active"
    step2_class = "done" if st.session_state.forgot_otp_verified else ("active" if st.session_state.forgot_otp_sent else "")
    step3_class = "active" if st.session_state.forgot_otp_verified else ""

    st.markdown(f"""
    <div class="auth-logo">
        <img src="data:image/png;base64,{logo_base64}">
    </div>

    <div class="auth-title">Reset Password</div>
    <div class="auth-subtitle" style="text-align: center; margin-bottom: 20px;">
        OTP VERIFICATION · EMAIL PROTECTED
    </div>
    
    <div class="step-indicator" style="margin-bottom: 25px;">
        <div class="step-dot {step1_class}">1</div>
        <span>Send OTP</span>
        <div class="step-line"></div>
        <div class="step-dot {step2_class}">2</div>
        <span>Verify</span>
        <div class="step-line"></div>
        <div class="step-dot {step3_class}">3</div>
        <span>New Password</span>
    </div>
    """, unsafe_allow_html=True)

    # STEP 1 & 2: Send and Verify OTP
    if not st.session_state.forgot_otp_verified:
        # Form for userid and email to send OTP
        if not st.session_state.forgot_otp_sent:
            with st.form("forgot_otp_request_form"):
                userid = st.text_input("UserID", placeholder="Enter your userID...")
                email = st.text_input("Email ID", placeholder="Enter your registered email...")
                submit_send = st.form_submit_button("Send OTP", key="send_otp_btn", use_container_width=True)

            if submit_send:
                if not userid or not email:
                    st.error("All fields are required ❌")
                    return
                
                userid_norm = userid.strip()
                email_norm = email.strip()

                # Find user
                try:
                    user = users_col.find_one({
                        "userid": {"$regex": f"^{re.escape(userid_norm)}$", "$options": "i"},
                        "email": {"$regex": f"^{re.escape(email_norm)}$", "$options": "i"}
                    })
                except Exception as e:
                    st.error("⚠️ Database connection error: Could not reach MongoDB Atlas. Please ensure your IP is whitelisted in MongoDB Atlas Network Access.")
                    return

                if not user:
                    st.error("User with specified UserID and Email not found ❌")
                    return

                if user.get("auth_provider") == "google":
                    st.error("This account uses Google login and cannot be reset here ❌")
                    return

                # Generate and send OTP
                otp = str(random.randint(100000, 999999))
                st.session_state.forgot_otp_code = otp
                st.session_state.forgot_otp_expiry = time.time() + 300
                st.session_state.forgot_otp_sent = True
                st.session_state.forgot_reset_email = user["email"]
                
                if send_forgot_otp_email(user["email"], otp):
                    st.success(f"OTP sent to **{user['email']}** ✅")
                    st.rerun()

        # Input to Verify OTP
        else:
            with st.form("forgot_otp_verify_form"):
                st.write(f"OTP has been sent to **{st.session_state.forgot_reset_email}**")
                otp_input = st.text_input("Enter OTP", placeholder="_ _ _ _ _ _", max_chars=6)
                col1, col_resend = st.columns([1, 1])
                with col1:
                    submit_verify = st.form_submit_button("Verify OTP", key="verify_otp_btn")
                with col_resend:
                    resend_clicked = st.form_submit_button("Resend OTP", key="resend_otp_btn")

            if resend_clicked:
                otp = str(random.randint(100000, 999999))
                st.session_state.forgot_otp_code = otp
                st.session_state.forgot_otp_expiry = time.time() + 300
                if send_forgot_otp_email(st.session_state.forgot_reset_email, otp):
                    st.success("New OTP sent successfully! ✅")
                    st.rerun()

            if submit_verify:
                if not otp_input:
                    st.warning("Please enter the OTP ⚠️")
                elif time.time() > st.session_state.forgot_otp_expiry:
                    st.error("OTP has expired ❌. Please click Resend OTP.")
                    st.session_state.forgot_otp_sent = False
                    st.session_state.forgot_otp_code = None
                    st.rerun()
                elif otp_input.strip() == st.session_state.forgot_otp_code:
                    st.session_state.forgot_otp_verified = True
                    st.success("OTP verified successfully! ✅")
                    st.rerun()
                else:
                    st.error("Incorrect OTP ❌")

    # STEP 3: Reset Password
    else:
        with st.form("forgot_password_reset_form"):
            st.info("🔓 Identity verified. Set your new password below.")
            new_password = st.text_input(
                "New Password",
                placeholder="Minimum 4 characters...",
                type="password"
            )
            confirm_password = st.text_input(
                "Confirm New Password",
                placeholder="Re-enter new password...",
                type="password"
            )
            submit_reset = st.form_submit_button("Reset Password", key="reset_btn", use_container_width=True)

        if submit_reset:
            if not new_password or not confirm_password:
                st.error("All fields are required ❌")
                return

            if len(new_password) < 4:
                st.error("Password must be at least 4 characters ❌")
                return

            if new_password != confirm_password:
                st.error("Passwords do not match ❌")
                return

            # Update password
            try:
                users_col.update_one(
                    {"email": st.session_state.forgot_reset_email},
                    {"$set": {"password": hash_password(new_password)}}
                )
            except Exception as e:
                st.error("⚠️ Database connection error: Could not reach MongoDB Atlas. Please ensure your IP is whitelisted in MongoDB Atlas Network Access.")
                return
            
            # Reset all OTP state variables
            for k in ["forgot_otp_code", "forgot_otp_expiry", "forgot_otp_verified", "forgot_otp_sent", "forgot_reset_email"]:
                st.session_state[k] = None if k in ["forgot_otp_code", "forgot_otp_expiry"] else False
                
            st.success("Password reset successfully! ✅ Please login with your new password.")
            
            # Auto switch tab back to login and rerun
            st.session_state.auth_tab = "login"
            st.rerun()

    # -------- BACK TO LOGIN LINK --------
    st.markdown("""
    <div style="text-align: center; margin-top: 15px;">
        <a href="?action=login" target="_self" style="color: #ffffff; text-decoration: underline; font-weight: 600; font-size: 14px;">Back to Login</a>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# AUTH RENDER
# =========================================================
def render_auth():
    handle_google_callback()
    
    # Intercept query parameters for navigation/error handling
    action = st.query_params.get("action")
    if action == "forgot_password":
        st.session_state.auth_tab = "forgot_password"
        # Reset OTP states when entering the screen fresh
        for k in ["forgot_otp_code", "forgot_otp_expiry", "forgot_otp_verified", "forgot_otp_sent", "forgot_reset_email"]:
            st.session_state[k] = None if k in ["forgot_otp_code", "forgot_otp_expiry"] else False
        st.query_params.clear()
    elif action == "login":
        st.session_state.auth_tab = "login"
        st.query_params.clear()

    error = st.query_params.get("error")
    if error == "google_not_configured":
        st.error("❌ Google Login is not configured. Please add `google_oauth` credentials to your Streamlit secrets.")
        st.query_params.clear()

    st.sidebar.empty()

    st.markdown("""
    <style>

    /* ---------- AUTH LOGO ---------- */
.auth-logo {
    width: 90px;
    height: 90px;
    margin: 0 auto 14px auto;

    border-radius: 50%;
    overflow: hidden;

    display: flex;
    align-items: center;
    justify-content: center;

    border: 2px solid rgba(255,255,255,0.25);
    box-shadow: 0 0 30px rgba(255,255,255,0.15);
}

.auth-logo img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* ---------- CENTER ALL FORM BUTTONS ---------- */
div[data-testid="stFormSubmitButton"] {
    width: 100% !important;
    display: block !important;
}

/* ---------- PRIMARY AUTH BUTTON (LOGIN / SIGNUP) ---------- */
div[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    height: 48px !important;
    margin-top: 14px !important;
    border-radius: 12px !important;        
    background: #ffffff !important;
    color: #000000 !important;
    font-family: 'Space Grotesk', -apple-system, sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    letter-spacing: 0.02em !important;
    border: 1px solid #ffffff !important;
    cursor: pointer !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    box-sizing: border-box !important;
}

/* Hover */
div[data-testid="stFormSubmitButton"] > button:hover {
    background: #e4e4e7 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 0 25px rgba(255, 255, 255, 0.35) !important;
}

/* Active */
div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.20) !important;
}

/* ================= TAB BUTTONS (LOGIN / SIGN UP) ================= */

/* Center tab buttons row */
div[data-testid="stHorizontalBlock"] {
    justify-content: center !important;
    gap: 12px;
}

/* ---------------- BASE TAB BUTTON (IDLE) ---------------- */
/* Must override Streamlit default styles */
div[data-testid="stButton"] > button {
    height: 44px !important;
    width: 100% !important;

    border-radius: 10px !important;
    background: linear-gradient(
        180deg,
        rgba(255,255,255,0.08),
        rgba(255,255,255,0.03)
    ) !important;

    border: 1px solid rgba(255,255,255,0.15) !important;
    color: #e5e7eb !important;

    font-weight: 700 !important;
    letter-spacing: 0.3px !important;

    transition: all 0.25s ease !important;
}

/* ---------------- HOVER STATE ---------------- */
div[data-testid="stButton"] > button:hover {
    background: linear-gradient(90deg, #ffffff, #404040) !important;
    border-color: rgba(255,255,255,0.30) !important;
    box-shadow: 0 10px 24px rgba(255,255,255,0.15) !important;
    transform: translateY(-1px);
}

/* ---------------- ACTIVE / SELECTED TAB ---------------- */
/* Use :focus-visible so it persists after click */
div[data-testid="stButton"] > button:focus-visible {
    background: linear-gradient(90deg, #ffffff, #525252) !important;
    color: #ffffff !important;
    border: none !important;
    box-shadow: 0 12px 28px rgba(255,255,255,0.25) !important;
}

/* Remove ugly focus outline */
div[data-testid="stButton"] > button:focus {
    outline: none !important;
}


    /* ---------- AUTH CARD ---------- */
    .auth-card {
        width: 420px;
        padding: 34px 32px;
        border-radius: 22px;
        background: linear-gradient(
            180deg,
            rgba(255,255,255,0.10),
            rgba(255,255,255,0.03)
        );
        border: 1px solid rgba(255,255,255,0.14);
        backdrop-filter: blur(18px);
        box-shadow:
            0 30px 60px rgba(0,0,0,0.55),
            inset 0 1px 0 rgba(255,255,255,0.06);
        animation: authFade 0.6s ease;
    }

    @keyframes authFade {
        from { opacity: 0; transform: translateY(14px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* ---------- TITLES ---------- */
    .auth-title {
        font-size: 26px;
        font-weight: 900;
        text-align: center;
        margin-bottom: 6px;
        background: linear-gradient(90deg, #ffffff, #404040);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .auth-subtitle {
        text-align: center;
        font-size: 14px;
        color: #9ca3af;
        margin-bottom: 26px;
    }

    /* ---------- INPUTS ---------- */
    div[data-testid="stTextInput"] input {
        height: 48px;
        border-radius: 14px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        color: #e5e7eb;
    }

    /* ---------- BUTTONS ---------- */
    div[data-testid="stButton"] button {
        height: 48px;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05) !important;
        color: #ffffff !important;
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        font-weight: 700;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.25s ease !important;
    }
    div[data-testid="stButton"] button:hover {
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(255, 255, 255, 0.35) !important;
        transform: translateY(-2px);
    }

    /* ---------- GOOGLE ---------- */
    .google-btn {
        width: 100% !important;
        height: 48px !important;
        border-radius: 12px !important;
        background: #ffffff !important;
        color: #000000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 10px !important;
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        letter-spacing: 0.02em !important;
        cursor: pointer !important;
        border: 1px solid #ffffff !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-sizing: border-box !important;
    }
    .google-btn:hover {
        background: #e4e4e7 !important;
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.35) !important;
        transform: translateY(-2px) !important;
    }

    /* ---------- REMOVE SIDEBAR ---------- */
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    /* REMOVE STREAMLIT FORM BORDER */
    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
        box-shadow: none !important;
    }

    /* ================= GLOBAL BACKGROUND & ANIMATION ================= */

    html, body, [data-testid="stApp"] {
        min-height: 100vh !important;
        background-color: #000000 !important;
        color: #e5e7eb;
        position: relative;
        overflow-x: hidden;
    }

    [data-testid="stApp"]::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            radial-gradient(1100px 650px at 50% 12%, rgba(255, 255, 255, 0.055) 0%, transparent 60%),
            radial-gradient(750px 450px at 15% 85%, rgba(255, 255, 255, 0.035) 0%, transparent 55%),
            radial-gradient(850px 500px at 85% 75%, rgba(255, 255, 255, 0.03) 0%, transparent 50%),
            linear-gradient(rgba(255, 255, 255, 0.018) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.018) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 100% 100%, 48px 48px, 48px 48px;
        animation: gridDrift 22s linear infinite;
        z-index: 0;
    }

    @keyframes gridDrift {
        0% { background-position: 0 0, 0 0, 0 0, 0 0, 0 0; }
        50% { background-position: 0 0, 0 0, 0 0, 24px 24px, 24px 24px; }
        100% { background-position: 0 0, 0 0, 0 0, 48px 48px, 48px 48px; }
    }

    @keyframes pulseHalo {
        0%, 100% {
            transform: translate(-50%, -50%) scale(0.95);
            opacity: 0.45;
        }
        50% {
            transform: translate(-50%, -50%) scale(1.15);
            opacity: 0.85;
        }
    }


/* Remove default Streamlit white layers */
section.main > div {
    background: transparent !important;
}

/* Remove Streamlit header spacing */
header {
    background: transparent !important;
}

/* Remove footer gap */
footer {
    visibility: hidden;
}
/* ================= TEXT INPUTS — THEME MATCHED ================= */

/* Input wrapper - ensure rounded corners */
div[data-testid="stTextInput"] {
    border-radius: 14px !important;
    overflow: visible !important;
    border: none !important;
}

div[data-testid="stTextInput"] > div,
div[data-testid="stTextInput"] [data-baseweb="base-input"],
div[data-testid="stTextInput"] [data-baseweb="input"] {
    border-radius: 14px !important;
    overflow: visible !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

div[data-testid="stTextInput"] input {
    height: 40px;
    padding: 0 16px;

    border-radius: 14px !important;

    /* Dark theme-matched background */
    background: rgba(255, 255, 255, 0.04);

    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #f4f4f5;

    font-size: 14px;
    font-weight: 500;

    transition: all 0.25s ease;
}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder {
    color: #71717a;
    font-weight: 400;
}

/* Hover */
div[data-testid="stTextInput"] input:hover {
    border-color: rgba(255, 255, 255, 0.35);
}

/* Focus (active typing) */
div[data-testid="stTextInput"] input:focus {
    outline: none !important;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.12) !important;
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: #ffffff !important;
}

/* Remove red invalid outline */
div[data-testid="stTextInput"] input:invalid {
    box-shadow: none !important;
    outline: none !important;
}

/* Remove focus-visible outline (keyboard focus) */
div[data-testid="stTextInput"] input:focus-visible {
    outline: none !important;
    box-shadow: 0 0 15px rgba(255, 255, 255, 0.12) !important;
    border-color: #ffffff !important;
}

/* Remove browser autofill highlight */
div[data-testid="stTextInput"] input:-webkit-autofill,
div[data-testid="stTextInput"] input:-webkit-autofill:hover,
div[data-testid="stTextInput"] input:-webkit-autofill:focus,
div[data-testid="stTextInput"] input:-webkit-autofill:active {
    box-shadow: 0 0 0 1000px #09090b inset !important;
    -webkit-text-fill-color: #e5e7eb !important;
}

/* Disabled */
div[data-testid="stTextInput"] input:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

/* Remove focus/invalid styling on the input container */
div[data-testid="stTextInput"]:focus-within,
div[data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
div[data-testid="stTextInput"] [data-baseweb="input"]:focus,
div[data-testid="stTextInput"] [data-baseweb="input"]:invalid {
    box-shadow: none !important;
    outline: none !important;
    border: none !important;
    border-radius: 14px !important;
}

/* Remove any additional wrapper borders */
div[data-testid="stTextInput"] > div > div,
div[data-testid="stTextInput"] [data-baseweb="base-input"] > div {
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
}

/* Hide "Press Enter to submit form" text */
div[data-testid="stTextInput"] [data-testid="InputInstructions"],
div[data-testid="stTextInput"] .stTextInput-instructions,
div[data-testid="InputInstructions"] {
    display: none !important;
    visibility: hidden !important;
}

div[data-testid="stTextInput"] [data-baseweb="input"]{
    box-shadow: none !important;
    outline: none !important;
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

    </style>
    """, unsafe_allow_html=True)

    # Initialize session state variables for forgot password OTP flow
    for k, v in [("forgot_otp_code", None), ("forgot_otp_expiry", None), ("forgot_otp_verified", False), ("forgot_otp_sent", False), ("forgot_reset_email", "")]:
        if k not in st.session_state:
            st.session_state[k] = v

    if "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"

    # ---------- CENTER USING COLUMNS ----------
    left, center, right = st.columns([3.5, 5.0, 3.5])

    with center:
        # ---------- TAB BUTTONS ----------
        c1, c2 = st.columns(2)

        with c1:
            if st.button("Login", key="auth_tab_login_btn", use_container_width=True):
                st.session_state.auth_tab = "login"
                st.rerun()

        with c2:
            if st.button("Sign Up", key="auth_tab_signup_btn", use_container_width=True):
                st.session_state.auth_tab = "signup"
                st.rerun()

        # ---------- CONTENT ----------
        if st.session_state.auth_tab == "login":
            login_view()
        elif st.session_state.auth_tab == "signup":
            signup_view()
        elif st.session_state.auth_tab == "forgot_password":
            forgot_password_view()

        st.caption(
            "© 2026 Apex Stock Screener • FinTech Analytics Platform • Built with Python & Streamlit"
        )


# =========================================================
# APP ENTRY (only when running this file directly)
if __name__ == "__main__":
    if not st.session_state.logged_in:
        render_auth()
    else:
        st.success("✅ Logged in! Redirect to dashboard here")