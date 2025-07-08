from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/stocks/(?P<symbol>[a-zA-Z0-9\-]+)/$', consumers.StockConsumer.as_asgi()),
    re_path(r'ws/test/$', consumers.TestConsumer.as_asgi()),
]