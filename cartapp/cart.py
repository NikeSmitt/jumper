from django.conf import settings
from django.urls import reverse

from mainapp.models.product import Product
from mainapp.models.size import Size
from django.shortcuts import get_object_or_404


class Cart:
    """Корзина для товаров"""
    
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(settings.CART_SESSION_ID, {})
        # print(self.cart or 'Nope')
    
    def add(self, product: Product, quantity=1, size_id=None, update=False):
        product_id = str(product.id)
        size = get_object_or_404(Size, id=size_id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'id': product_id,
                'product_name': product.name,
                'price': product.price,
                'quantity': 0,
                'url': product.get_absolute_path(),
                'image': product.images.first().image.url,
                'size_id': size_id,
                'size': size.value,
                'size_label': size.label_shoes if size.label_shoes else size.label_clothes
            }
        if update:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        self.save()
        
    def clear_cart(self):
        """Очищаем корзину"""
        self.cart = {}
        self.save()
    
    def remove(self, product: Product):
        """Удаление продукта из корзины"""
        product_id = str(product.id)
        if product_id not in self.cart:
            print(f'Error: {product_id} -> {product.name} not in cart!')
        else:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        for item in self.cart.values():
            item['total_price'] = float(item['price']) * float(item['quantity'])
            yield item
    
    def __len__(self):
        return sum(int(value['quantity']) for value in self.cart.values())
        # return sum(item['quantity'] for item in self.cart.values())
    
    def get_total(self):
        """Получаем стоимость всей корзины"""
        return sum(float(item['price']) * float(item['quantity']) for item in self.cart.values())
    
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    
    # def __del__(self):
    #     print('Cart deleted')
