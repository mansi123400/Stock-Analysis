# 📈 Stock Market Dashboard

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Yahoo Finance](https://img.shields.io/badge/Yahoo%20Finance-6001D2?style=for-the-badge&logo=yahoo&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Free API](https://img.shields.io/badge/API-100%25%20Free-brightgreen?style=for-the-badge)
![Markets](https://img.shields.io/badge/Markets-Global-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

### 🚀 A powerful, real-time stock market dashboard — completely free, no paid API needed!

[Features](#-features) • [Demo](#-demo-preview) • [Getting Started](#-getting-started) • [Tickers](#-supported-ticker-formats) • [Contributing](#-contributing)

</div>

---

## 🖥️ Demo Preview

> 💡 Type any stock ticker (e.g. `AAPL`, `RELIANCE.NS`, `BTC-USD`) and instantly get live charts, technical indicators, and real company logo!

---

## ✨ Features

<table>
<tr>
<td>

### 📊 Charts & Visualization
- 🕯️ Candlestick & Line charts
- 📉 Volume bars subplot
- 📐 SMA 20 & 50 day overlays
- 🎨 Clean Plotly white theme

</td>
<td>

### 🔬 Technical Indicators
- 📡 RSI (14-day)
- 〽️ MACD & Signal line
- 📎 Bollinger Bands
- 📊 Returns histogram

</td>
</tr>
<tr>
<td>

### 🌍 Global Market Support
- 🇺🇸 US Stocks (NYSE, NASDAQ)
- 🇮🇳 Indian Stocks (NSE & BSE)
- 🇬🇧 UK Stocks (LSE)
- ₿ Cryptocurrency

</td>
<td>

### ⚡ Smart Features
- 🏢 Auto company logo fetch
- 🔀 Multi-stock comparison
- 📥 CSV data export
- 💹 Key metrics cards

</td>
</tr>
</table>

---

## 🛠️ Tech Stack

<div align="center">

| Tool | Purpose | Version |
|------|---------|---------|
| ![Streamlit](https://img.shields.io/badge/-Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white) | Web app framework | Latest |
| ![yfinance](https://img.shields.io/badge/-yfinance-6001D2?style=flat&logo=yahoo&logoColor=white) | Free Yahoo Finance API | Latest |
| ![Plotly](https://img.shields.io/badge/-Plotly-3F4F75?style=flat&logo=plotly&logoColor=white) | Interactive charts | Latest |
| ![Pandas](https://img.shields.io/badge/-Pandas-150458?style=flat&logo=pandas&logoColor=white) | Data processing | Latest |
| ![Requests](https://img.shields.io/badge/-Requests-2CA5E0?style=flat&logo=python&logoColor=white) | Logo fetching | Latest |

</div>

---

## 🚀 Getting Started

### ✅ Prerequisites

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Git](https://img.shields.io/badge/Git-required-orange?style=flat-square&logo=git)

### 📥 Step 1 — Clone the repository

```bash
git clone https://github.com/your-username/stock-market-dashboard.git
cd stock-market-dashboard
```

### 📦 Step 2 — Install dependencies

```bash
pip install streamlit yfinance plotly pandas requests
```

### ▶️ Step 3 — Run the app

```bash
streamlit run app.py
```

> 🌐 The app will open automatically at `http://localhost:8501`

---

## 📦 Project Structure

```
📁 stock-market-dashboard/
│
├── 🐍 app.py                  # Main Streamlit application
├── 📋 requirements.txt        # Python dependencies
└── 📖 README.md               # Project documentation
```

---

## 🎯 Supported Ticker Formats

<div align="center">

| 🌍 Market | 📝 Format | 💡 Example |
|-----------|-----------|------------|
| 🇺🇸 US Stocks | `TICKER` | `AAPL`, `TSLA`, `NVDA`, `GOOGL` |
| 🇮🇳 Indian NSE | `TICKER.NS` | `RELIANCE.NS`, `TCS.NS`, `INFY.NS` |
| 🇮🇳 Indian BSE | `TICKER.BO` | `INFY.BO`, `WIPRO.BO`, `SBIN.BO` |
| 🇬🇧 UK Stocks | `TICKER.L` | `HSBA.L`, `BP.L`, `SHEL.L` |
| ₿ Crypto | `TICKER-USD` | `BTC-USD`, `ETH-USD`, `DOGE-USD` |

</div>

---

## 📊 Technical Indicators Explained

| Indicator | Description | Signal |
|-----------|-------------|--------|
| 📈 **SMA 20** | 20-day Simple Moving Average | Short-term trend |
| 📈 **SMA 50** | 50-day Simple Moving Average | Long-term trend |
| 📡 **RSI (14)** | Relative Strength Index | >70 Overbought / <30 Oversold |
| 〽️ **MACD** | Moving Average Convergence Divergence | Momentum signal |
| 📎 **Bollinger Bands** | Volatility bands around SMA | Price extremes |
| 📐 **Sharpe Ratio** | Risk-adjusted return (annualized) | Higher = better |

---

## 🌐 Logo Fetching — How It Works

```
Ticker Entered
      │
      ▼
┌─────────────────────┐
│  Layer 1: yfinance  │ ──✅ Found → Display Logo
│  logo_url field     │
└─────────────────────┘
      │ ❌ Not Found
      ▼
┌─────────────────────┐
│  Layer 2: Clearbit  │ ──✅ Found → Display Logo
│  via company domain │
└─────────────────────┘
      │ ❌ Not Found
      ▼
┌─────────────────────┐
│  Layer 3: logo.dev  │ ──✅ Found → Display Logo
│  via ticker symbol  │
└─────────────────────┘
      │ ❌ All Failed
      ▼
   🏢 Emoji Fallback
```

> 🔑 **No API key required for any layer!**

---

## 📋 requirements.txt

```txt
streamlit
yfinance
plotly
pandas
requests
```

---

## 🤝 Contributing

1. 🍴 **Fork** the repository
2. 🌿 **Create** a new branch (`git checkout -b feature/AmazingFeature`)
3. 💾 **Commit** your changes (`git commit -m 'Add AmazingFeature'`)
4. 📤 **Push** to the branch (`git push origin feature/AmazingFeature`)
5. 🔃 **Open** a Pull Request

> 🐛 Found a bug? Open an [Issue](https://github.com/mansi123400/stock-market-dashboard/issues)

---

## 📄 License

```
MIT License — free to use, modify, and distribute.
```

![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 👨‍💻 Author

<div align="center">

Built with ❤️ and ☕ using Python & Streamlit

[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github)](https://github.com/mansi123400)

### ⭐ Star this repo if you found it useful!

![Star](https://img.shields.io/github/stars/mansi123400/stock-market-dashboard?style=social)

</div>

---

## ⚠️ Disclaimer

> This app is for **educational and informational purposes only**.
> It is **not financial advice**. Always do your own research before making any investment decisions.

---

<div align="center">

![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f?style=for-the-badge&logo=python)
![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=for-the-badge)

</div>
