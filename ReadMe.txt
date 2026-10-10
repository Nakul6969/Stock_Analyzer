Tech Stack covered:

✅ Python & Streamlit
✅ MongoDB (Database design)
✅ REST APIs (IndianAPI, AI Analyzer)
✅ Authentication system (JWT-style sessions)
✅ Google OAuth 2.0
✅ Email OTP system (SMTP)
✅ Bcrypt password hashing (Security)

Concepts demonstrated:

✅ Full-stack development
✅ Database CRUD operations
✅ API integration
✅ Security best practices
✅ Multi-page application architecture
✅ Real-time financial data


How to present it on resume:
Apex Stock Screener
- Built full-stack stock analysis web app using Python & Streamlit
- Integrated Indian API for real-time Nifty50, IPO & mutual fund data
- Implemented secure auth system with Google OAuth, bcrypt & email OTP
- Used MongoDB Atlas for user management and data persistence
- Deployed on Streamlit Cloud with CI/CD via GitHub

------------------------------------IMP--------------------------------------------------------------

When you're ready to deploy, remember:

🗄️ Migrate to MongoDB Atlas
🔗 Update MONGO_URI in both .env and secrets.toml

Also add the deployed URL in Google Cloud Console:
1. Go to → Google Cloud Console → APIs & Services → Credentials
2. Click your **Apex Web Client**
3. Under **Authorized redirect URIs** → **Add URI:**

https://yourapp.streamlit.app

4. Click **Save**
------------------------------------------------------------------------------------------------------

**So deployment checklist:**
```
✅ 1. Create Atlas cluster → get Atlas URI
✅ 2. Update MONGO_URI in secrets.toml → Atlas URI
✅ 3. Update redirect_uri in secrets.toml → deployed URL
✅ 4. Add deployed URL in Google Cloud Console
✅ 5. Add all secrets in Streamlit Cloud dashboard
        (Settings → Secrets → paste entire secrets.toml)
✅ 6. Deploy!