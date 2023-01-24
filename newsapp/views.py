from django.shortcuts import render
from django.views.generic import DetailView, ListView

from newsapp.models import NewsItem, NewsCategory, NewsTag


class NewsView(DetailView):
    model = NewsItem
    template_name = 'newsapp/news-post.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = NewsItem.objects.order_by('-created_at')
        context['news_categories'] = NewsCategory.objects.all()
        context['tags'] = NewsTag.objects.all()
        return context
    
    
class NewsListView(ListView):
    template_name = ''
    context_object_name = 'news_list'
    
    