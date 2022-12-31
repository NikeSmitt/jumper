from mainapp.views import IndexView, ProductListView
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/<slug:slug>', ProductListView.as_view(), name='product_list'),
]