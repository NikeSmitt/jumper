from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from cartapp.cart import Cart
from mainapp.models.product import Product
from mainapp.models.size import Size
from orderapp.forms import LogoutCreateOrderForm
from orderapp.models import Order, OrderItem


class CreateOrderView(View):
    """Страница с оформлением заказа"""
    
    checkout_template = 'orderapp/checkout.html'
    confirm_template = 'orderapp/confirm.html'
    
    def post(self, request):
        form = LogoutCreateOrderForm(request.POST)
        context = {
            'form': form,
            'cart': Cart(request),
        }
        if form.is_valid():
            cart = Cart(request)
            order = form.save()
            
            for item in cart:
                product = get_object_or_404(Product, id=item['id'])
                quantity = item.get('quantity')
                size_id = item.get('size_id')
                size = get_object_or_404(Size, id=size_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity, size=size)
                
            cart.clear_cart()
            return render(request, template_name=self.confirm_template)
        else:
            
            return render(request, self.checkout_template, context=context)
    
    def get(self, request):
        form = LogoutCreateOrderForm()
        cart = Cart(request)
        context = {
            'form': form,
            'cart': cart,
        }
        return render(request, self.checkout_template, context=context)
