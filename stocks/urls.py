from django.urls import path
from . import views

urlpatterns = [
    path('', views.stock_search, name='stock_search'),
]