from django.conf import settings
from django.shortcuts import render
from django.views import View

from cartapp.cart import Cart


class CartView(View):
    """Корзина пользователя"""
    template_name = 'cart.html'
    
    def get(self, request):
        context = {}
        cart_items = Cart(request)
        context = {
            'cart_items': cart_items,
        }
        
        return render(request, self.template_name, context=context)
