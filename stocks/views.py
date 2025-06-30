from django.shortcuts import render

def stock_search(request):
    stock_data = None
    if request.method == 'POST':
        ticker = request.POST.get('ticker')
        # Simulated API response (you'll replace this later with real data)
        stock_data = {
            'ticker': ticker.upper(),
            'name': 'Example Corp.',
            'price': 123.45,
        }
    return render(request, 'stocks/stock_search.html', {'stock_data': stock_data})
