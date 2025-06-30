import requests
from django.conf import settings
from django.shortcuts import render

def stock_search(request):
    stock_data = None
    error = None

    if request.method == 'POST':
        ticker = request.POST.get('ticker').upper()
        api_key = settings.FINNHUB_API_KEY
        url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"

        try:
            response = requests.get(url)
            data = response.json()
            print(data)

            if response.status_code == 200 and data.get("c"):
                stock_data = {
                    'ticker': ticker,
                    'current': data['c'],
                    'open': data['o'],
                    'high': data['h'],
                    'low': data['l'],
                    'prev_close': data['pc'],
                    'change': data['d'],
                    'percent_change': data['dp']
                }
            else:
                error = f"No data found for '{ticker}'."
        except Exception as e:
            error = f"Error fetching data: {str(e)}"

    return render(request, 'stocks/stock_search.html', {
        'stock_data': stock_data,
        'error': error
    })
