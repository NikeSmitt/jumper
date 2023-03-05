from django.conf import settings
from django.core.mail import send_mail
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
            send_email_order_creation(order)
            
            
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


def send_email_order_creation(order: Order):
    # sending email
    products = [str(o) for o in order.order_items.all()]
    
    products_to_str = '\n'.join(products)
    message = f"""
    f'Просмотрите содержимое заказа'
        f'Номер заказа - {order.order_number}'
        f'Имя клиента - {order.first_name}'
        f'Телефон - {order.phone}'
        f'Email - {order.email}'
        f'Дополнения к заказу - {order.comment}'
        f'Товары в заказе - {products_to_str}',
    """
    send_mail(
        subject=f'Заказ {order.order_number} создан {order.created_at.strftime("%m/%d/%Y, %H:%M:%S")}',
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=settings.ADMIN_EMAILS,
        fail_silently=False,
    )