import requests
from django.conf import settings
from django.shortcuts import render
from datetime import datetime, timezone
import json
import pprint

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
            articles = news_response.get("articles", [])
            for article in articles:
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

                news.append({
                    'title': title,
                    'url': url,
                    'source': source,
                    'published': published_dt,
                    'image': image_url
                })

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


# STOCK SEARCH VIEW
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

            stats_data = {
                'exchange': quote_response.get('exchange', '-'),
                'volume': int(quote_response.get('volume', 0)),
                'prev_close': float(quote_response.get('previous_close', 0)),
                'open': float(quote_response.get('open', 0)),
                'high': float(quote_response.get('high', 0)),
                'low': float(quote_response.get('low', 0)),
            }

            # Related News
            if company_name:
                news_url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&pageSize=5&apiKey={news_api_key}"
                news_response = requests.get(news_url).json()
                if news_response.get("status") == "ok":
                    articles = news_response.get("articles", [])
                    for article in articles:
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
        'error': error,
    })
