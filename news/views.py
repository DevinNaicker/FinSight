import requests
from django.conf import settings
from django.shortcuts import render
from datetime import datetime, timezone
import math

def news_feed(request):
    articles = []
    error = None

    # Get page number from URL (default to 1)
    page = int(request.GET.get("page", 1))
    page_size = 10

    url = (
        f"https://newsapi.org/v2/everything?"
        f"q=finance&language=en&sortBy=publishedAt&pageSize={page_size}&page={page}&apiKey={settings.NEWS_API_KEY}"
    )

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and data.get("articles"):
            for article in data["articles"]:
                # Parse publishedAt to datetime
                published_at = article.get("publishedAt")
                if published_at:
                    try:
                        dt = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
                        article["publishedAt"] = dt.replace(tzinfo=timezone.utc)
                    except Exception:
                        article["publishedAt"] = None
                else:
                    article["publishedAt"] = None

                articles.append(article)

            total_results = data.get("totalResults", 0)
            total_pages = math.ceil(total_results / page_size)
        else:
            error = data.get("message", "Failed to fetch news.")
            total_pages = 1
    except Exception as e:
        error = f"Error: {str(e)}"
        total_pages = 1

    return render(request, "news/news_feed.html", {
        "articles": articles,
        "error": error,
        "current_page": page,
        "has_next": page < total_pages,
    })
