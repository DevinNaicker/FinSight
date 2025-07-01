import requests
from django.conf import settings
from django.shortcuts import render
import time
import json

def stock_search(request):
    stock_data = None
    chart_data = None
    error = None

    if request.method == 'POST':
        ticker = request.POST.get('ticker').upper()
        api_key = settings.TWELVE_DATA_API_KEY

        try:
            # 📈 Real-time quote
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

            # 🕓 7-day historical data
            now = time.strftime('%Y-%m-%d')
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
