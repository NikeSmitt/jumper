from django.urls import path
from .views import NewsView, NewsListView

app_name = 'newsapp'

urlpatterns = [
    path('<slug:slug>/', NewsView.as_view(), name='news'),
    path('category/', NewsListView.as_view(), name='news_list'),
]