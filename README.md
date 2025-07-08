# 📊 FinSight

**FinSight** is a modern web application for tracking live stock and currency prices, discovering market trends, and staying updated with the latest financial news — all in one interactive platform.

---

## 🚀 Features

- 🔍 **Predictive Stock Search**  
  Search by ticker or company name with real-time suggestions.

- 💹 **Live Currency Prices via WebSocket**  
  Real-time updates for popular currency pairs like BTC/USD and EUR/USD using the Twelve Data WebSocket API.

- 📈 **Popular Stock Cards**  
  Display live stock prices and daily performance for top tickers like AAPL, TSLA, AMZN, etc.

- 📰 **Curated Financial News Feed**  
  Latest business headlines fetched from NewsAPI, with human-friendly timestamps.

- 📊 **Stock Detail Pages**  
  Includes recent chart data, stats (e.g., P/E, EPS), and related news per company.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** HTML5, Bootstrap 5, JavaScript  
- **Live Data:**  
  - Stock & currency data from [Twelve Data](https://twelvedata.com/)  
  - News from [NewsAPI](https://newsapi.org/)  
- **WebSockets:** Django Channels + Daphne  
- **Database:** SQLite (for development)  
- **Hosting:** Localhost (development environment)

---

## 🧪 Getting Started (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/finsight.git
cd finsight
