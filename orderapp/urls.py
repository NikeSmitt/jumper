from django.urls import path
from .views import CreateOrderView

app_name = 'orderapp'

urlpatterns = [
    path('checkout/', CreateOrderView.as_view(), name='checkout'),
    # path('create/', CreateOrderView.as_view(), name='create'),
]