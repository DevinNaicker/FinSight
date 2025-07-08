# 📊 FinSight
![logo](images/FinSight.png)
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
```
### 2. Create a virtual environment and activate it
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
### 3. Install dependencies
```
pip install -r requirements.txt
```
### 4. Set environment variables

Create a .env file or export these in your shell:
```
TWELVE_DATA_API_KEY=your_twelve_data_api_key
NEWS_API_KEY=your_newsapi_key
```
Alternatively, you can define these in settings.py for development.

### 5. Run migrations
```
python manage.py migrate
```
### 6. Start the Django development server
```
python manage.py runserver
```
### 7. Run the WebSocket worker

In a separate terminal tab/window:
```
python manage.py run_twelve_ws
```

## 📸 Screenshots

_(Add screenshots of your homepage, stock view, and WebSocket live updates here.)_

---

## ✅ Future Enhancements

- Add user login and personal watchlists  
- Historical chart comparison tools  
- Deployment to AWS or Railway  
- Multi-currency support with exchange selection  
- Improved mobile responsiveness  

---

## 👨‍💻 Author

**Thirushan Devin Naicker**  
Finance graduate turned software developer.  
Passionate about fintech and building tools that make financial data accessible.

- GitHub: [@DevinNaicker](https://github.com/DevinNaicker)  
- LinkedIn: [Thirushan Naicker](https://www.linkedin.com/in/devin-naicker-659711a4)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
