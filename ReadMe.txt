# 📈 Apex Stock Screener

**Apex Stock Screener** is a full-stack Indian financial market intelligence and stock analysis web application built with **Python** and **Streamlit**. It provides real-time equity insights, Nifty 50 movers, IPO tracking, mutual funds & corporate bonds analytics, MCX commodities tracking, AI-powered stock briefings, and a Machine Learning risk-scoring engine.

---

## ✨ Key Features

- **🔍 Stock Insights & Fundamentals**: Real-time NSE/BSE stock quotes, interactive candlestick & DMA price charts, key valuation ratios (P/E, P/B, ROE, Debt-to-Equity), financial statements, and shareholding patterns.
- **🤖 Machine Learning Risk Predictor**: Custom **Random Forest Regressor** (`scikit-learn`) trained on 17 fundamental and technical indicators (Volatility, Beta, P/E, Debt/Equity, Margins, DMA ratios, 52W momentum) to predict a normalized **1–10 Stock Risk Score**.
- **🧠 AI Stock Analyzer**: Generates instant bull/bear investment cases, valuation summaries, and actionable executive briefings using LLM integration (Groq / Llama 3).
- **📊 Nifty 50 Market Movers**: Live market breadth, top gainers/losers, volume shockers, and 52-week high/low breakouts.
- **🎛️ Multi-Cap Stock Screener**: Filter stocks across **Large Cap**, **Mid Cap**, and **Small Cap** segments with interactive performance visualizers.
- **🏛️ IPOs, Mutual Funds & Bonds**: Track upcoming/listed IPOs, top-performing mutual funds across categories, and SGB/corporate bond yields.
- **🪙 Commodities Dashboard**: Live MCX futures contracts across Metals, Energy, and Agricultural commodities.
- **🔐 Secure Authentication**: Full user management backed by **MongoDB Atlas**, featuring **Google OAuth 2.0**, **Bcrypt** password hashing, and **SMTP Email OTP** verification.

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend & UI** | Streamlit, Custom Glassmorphism CSS, Plotly Interactive Charts |
| **Backend & Data** | Python, Pandas, NumPy, REST APIs (`IndianAPI.in`, `yfinance`) |
| **Machine Learning & AI** | Scikit-Learn (Random Forest Regressor), Joblib, Groq LLM API |
| **Database** | MongoDB Atlas (`pymongo`) |
| **Authentication & Security** | Google OAuth 2.0, `bcrypt` Password Hashing, Gmail SMTP OTP |

---

## 📂 Project Structure

```text
Apex-Stock-Screener/
├── ◈_Welcome.py              # Main entry point & authentication gateway
├── auth/                     # Login, Registration, Google OAuth & Email OTP handlers
├── data/                     # API clients, caching & market data fetchers
├── database/                 # MongoDB Atlas connection & user CRUD operations
├── ml/                       # Random Forest model training, features & risk predictor
├── pages/                    # Multi-page dashboard modules
│   ├── ◈_Stock_Insights.py
│   ├── ◩_Nifty50_Movers.py
│   ├── ◧_Commodities.py
│   ├── ◧_IPOs_Details.py
│   ├── ◧_Mutual_Funds_&_Bonds.py
│   ├── ◪_Stock_filter.py
│   ├── ✦_Ai_Analyzer.py
│   └── ⚙_Account_Settings.py
├── ui/                       # Global luxury theme styles & reusable UI components
└── requirements.txt          # Python dependencies
```

---

## 🚀 Getting Started Locally

### 1. Clone the repository
```bash
git clone https://github.com/Nakul6969/Stock_Analyzer.git
cd Stock_Analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a `.env` file in the root directory (and `.streamlit/secrets.toml` for OAuth/deployment):
```env
API_KEY=your_indian_api_key
GROQ_API_KEY=your_groq_api_key
MONGO_URI=your_mongodb_atlas_connection_string
EMAIL_ADDRESS=your_smtp_email
EMAIL_PASSWORD=your_smtp_app_password
```

### 4. Run the application
```bash
streamlit run ◈_Welcome.py
```

---

## ☁️ Deployment

Deployed on **Streamlit Community Cloud** with continuous deployment connected to GitHub and **MongoDB Atlas** cloud persistence.
