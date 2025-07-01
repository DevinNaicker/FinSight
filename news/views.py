import requests
from django.conf import settings
from django.shortcuts import render

def news_feed(request):
    articles = []
    error = None
    url = (
    f"https://newsapi.org/v2/everything?"
    f"q=finance&language=en&sortBy=publishedAt&pageSize=10&apiKey={settings.NEWS_API_KEY}"
)

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("articles"):
            articles = data["articles"]
        else:
            error = data.get("message", "Failed to fetch news.")
    except Exception as e:
        error = f"Error: {str(e)}"

    return render(request, "news/news_feed.html", {"articles": articles, "error": error})
