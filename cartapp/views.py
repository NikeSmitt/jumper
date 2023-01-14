from django.shortcuts import render
from django.views import View

from cartapp.cart import Cart


class CartView(View):
    """Корзина пользователя"""
    template_name = 'cart.html'
    
    def get(self, request):
        context = {}
        if not request.user.is_authenticated:
            c = Cart(request)
            cart_items = list(c.cart.values())
            print(cart_items)
            context = {
                'cart_items': cart_items,
            }
        
        return render(request, self.template_name, context=context)
