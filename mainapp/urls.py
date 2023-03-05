from cartapp.api import api_add_to_cart, api_get_cart_items, remove_cart_item
from mainapp.views import IndexView, ProductListView, ProductDetailView, ProductTagListView, ProductSearchListView
from django.urls import path

app_name = 'mainapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('catalog/<slug:slug>/', ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('tag/<slug:slug>/', ProductTagListView.as_view(), name='product_tag_list'),
    path('products/', ProductSearchListView.as_view(), name='product_search_list'),

    
    # API
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/get_cart_items/', api_get_cart_items, name='api_get_cart_items'),
    path('api/remove_cart_item/', remove_cart_item, name='api_remove_cart_item'),
]
