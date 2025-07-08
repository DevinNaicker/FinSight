import requests
from django.conf import settings
from django.shortcuts import render
from datetime import datetime, timezone
import json
from django.utils.safestring import mark_safe
from django.utils.text import slugify

# HOMEPAGE VIEW
def home(request):
    news = []
    popular_stocks = {}
    currency_data = {}
    slugged_currency_data = {}
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'NVDA']
    currencies = ['BTC/USD', 'EUR/USD']
    live_mode = False

    # Map currency pair → full name
    currency_full_names = {
        'BTC/USD': 'Bitcoin to United States Dollar',
        'EUR/USD': 'Euro to United States Dollar',
    }

    try:
        # News
        api_key = settings.NEWS_API_KEY
        news_url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&pageSize=5&apiKey={api_key}"
        news_response = requests.get(news_url).json()

        if news_response.get("status") == "ok":
            for article in news_response.get("articles", []):
                title = article.get('title', '')
                source = article.get('source', {}).get('name', '')
                url = article.get('url')
                published_at = article.get('publishedAt', '')
                image_url = article.get('urlToImage')

                if title.endswith(f" - {source}"):
                    title = title.rsplit(f" - {source}", 1)[0]

                published_dt = None
                if published_at:
                    try:
                        published_dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
                    except Exception as e:
                        print(f"Failed to parse publishedAt: {e}")

                news.append({
                    'title': title,
                    'url': url,
                    'source': source,
                    'published': published_dt,
                    'image': image_url
                })

        # Stocks
        if live_mode:
            for ticker in tickers:
                popular_stocks[ticker] = {
                    'price': 0.0,
                    'change': 0.0,
                    'abs_change': 0.0,
                    'percent': 0.0,
                    'name': ticker
                }
        else:
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
                        'name': stock.get('name', '')
                    }

        # Currencies (WebSocket placeholder)
        for pair in currencies:
            currency_data[pair] = {'price': 0.0}
            slug = pair.replace('/', '-').lower()
            slugged_currency_data[slug] = {
                'price': 0.0,
                'pair': pair,
                'display': currency_full_names.get(pair, pair)
            }

    except Exception as e:
        print(f"Homepage data fetch error: {e}")

    print("🚨 FINAL currencies:", currencies)
    print("🚨 FINAL currency_data keys:", list(currency_data.keys()))
    print("🚨 Slugged currency keys:", list(slugged_currency_data.keys()))
    print("✅ Slugged Currency Data:")
    for slug, data in slugged_currency_data.items():
        print(f"{slug}: {data}")

    return render(request, 'home.html', {
        'news': news,
        'popular_stocks': popular_stocks,
        'currency_data': currency_data,
        'slugged_currency_data': slugged_currency_data,
        'live_mode': live_mode,
        'tickers': mark_safe(json.dumps(list(popular_stocks.keys()))),
        'currencies': mark_safe(json.dumps(currencies)),
    })


# STOCK SEARCH VIEW (unchanged)
def stock_search(request):
    stock_data = None
    chart_data = None
    stats_data = None
    related_news = []
    error = None

    # Get ticker from either POST or GET
    if request.method == 'POST':
        ticker = request.POST.get('ticker', '').upper()
    else:
        ticker = request.GET.get('ticker', '').upper()

    if ticker:
        api_key = settings.TWELVE_DATA_API_KEY
        news_api_key = settings.NEWS_API_KEY

        try:
            # Quote
            quote_url = f"https://api.twelvedata.com/quote?symbol={ticker}&apikey={api_key}"
            quote_response = requests.get(quote_url).json()

            if "close" not in quote_response or "code" in quote_response:
                raise ValueError(quote_response.get("message", "Invalid ticker."))

            company_name = quote_response.get('name', '')

            stock_data = {
                'ticker': ticker,
                'name': company_name,
                'current': float(quote_response['close']),
                'open': float(quote_response['open']),
                'high': float(quote_response['high']),
                'low': float(quote_response['low']),
                'prev_close': float(quote_response['previous_close']),
                'change': float(quote_response['change']),
                'percent_change': float(quote_response['percent_change'])
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
                    'prices': json.dumps(prices)
                }

            stats_data = {
                'exchange': quote_response.get('exchange', '-'),
                'volume': int(quote_response.get('volume', 0)),
                'prev_close': float(quote_response.get('previous_close', 0)),
                'open': float(quote_response.get('open', 0)),
                'high': float(quote_response.get('high', 0)),
                'low': float(quote_response.get('low', 0))
            }

            # Related News
            if company_name:
                news_url = (
                    f"https://newsapi.org/v2/everything?"
                    f"q={company_name}&language=en&pageSize=5&apiKey={news_api_key}"
                )
                news_response = requests.get(news_url).json()

                if news_response.get("status") == "ok":
                    for article in news_response.get("articles", []):
                        title = article.get('title', '')
                        source = article.get('source', {}).get('name', '')
                        url = article.get('url')
                        published_at = article.get('publishedAt', '')
                        image_url = article.get('urlToImage')

                        if title.endswith(f" - {source}"):
                            title = title.rsplit(f" - {source}", 1)[0]

                        published_dt = None
                        if published_at:
                            try:
                                published_dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                                published_dt = published_dt.replace(tzinfo=timezone.utc)
                            except Exception as e:
                                print(f"Failed to parse publishedAt: {e}")

                        related_news.append({
                            'title': title,
                            'url': url,
                            'source': source,
                            'published': published_dt,
                            'image': image_url
                        })

        except Exception as e:
            error = str(e)
            print(f"Error fetching stock data: {error}")

    return render(request, 'stocks/stock_search.html', {
        'stock_data': stock_data,
        'chart_data': chart_data,
        'stats_data': stats_data,
        'related_news': related_news,
        'error': error
    })
