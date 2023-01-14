from django.urls import path
import cartapp.views as views

app_name = 'cartapp'

urlpatterns = [
    path('', views.CartView.as_view(), name='cart'),
]