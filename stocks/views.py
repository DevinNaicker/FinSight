import requests
from django.conf import settings
from django.shortcuts import render
import time
import json

# HOMEPAGE VIEW
def home(request):
    news = []
    popular_stocks = {}
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA']

    try:
        # News API
        api_key = settings.NEWS_API_KEY
        news_url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey={api_key}"
        news_response = requests.get(news_url).json()
        if news_response.get("status") == "ok":
            news = news_response.get("articles", [])

        # Popular Stocks API
        stock_api_key = settings.TWELVE_DATA_API_KEY
        symbols = ','.join(tickers)
        quote_url = f"https://api.twelvedata.com/quote?symbol={symbols}&apikey={stock_api_key}"
        stock_response = requests.get(quote_url).json()

        for ticker in tickers:
            stock = stock_response.get(ticker)
            if stock and "close" in stock:
                change = float(stock['change'])
                popular_stocks[ticker] = {
                    'price': float(stock['close']),
                    'change': change,
                    'abs_change': abs(change),
                    'percent': float(stock['percent_change']),
                    'name': stock.get('name', ''),
                }

    except Exception as e:
        print(f"Homepage data fetch error: {e}")

    return render(request, 'home.html', {
        'news': news,
        'popular_stocks': popular_stocks,
    })


# STOCK SEARCH VIEW — ⛔️ Not modified as per your request
def stock_search(request):
    stock_data = None
    chart_data = None
    error = None

    if request.method == 'POST':
        ticker = request.POST.get('ticker', '').upper()
        api_key = settings.TWELVE_DATA_API_KEY

        try:
            # Quote
            quote_url = f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={api_key}"
            quote_response = requests.get(quote_url).json()

            if "close" not in quote_response or "code" in quote_response:
                raise ValueError(quote_response.get("message", "Invalid ticker."))

            stock_data = {
                'ticker': ticker,
                'current': float(quote_response['close']),
                'open': float(quote_response['open']),
                'high': float(quote_response['high']),
                'low': float(quote_response['low']),
                'prev_close': float(quote_response['previous_close']),
                'change': float(quote_response['change']),
                'percent_change': float(quote_response['percent_change']),
            }

            # Chart Data
            history_url = f"https://api.twelvedata.com/time_series?symbol={ticker}&interval=1day&outputsize=7&apikey={api_key}"
            history_response = requests.get(history_url).json()

            if "values" in history_response:
                history = history_response["values"]
                labels = [entry["datetime"] for entry in reversed(history)]
                prices = [float(entry["close"]) for entry in reversed(history)]

                chart_data = {
                    'labels': json.dumps(labels),
                    'prices': json.dumps(prices),
                }

        except Exception as e:
            error = str(e)

    return render(request, 'stocks/stock_search.html', {
        'stock_data': stock_data,
        'chart_data': chart_data,
        'error': error,
    })
