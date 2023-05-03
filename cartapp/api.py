import json

from django.http import JsonResponse

from cartapp.cart import Cart
from django.shortcuts import get_object_or_404

from mainapp.models.product import Product


def api_add_to_cart(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        cart = Cart(request)
        for product_data in data.get('products'):
            product = get_object_or_404(Product, pk=product_data['id'])
            size_id = product_data.get('size_id')
            update = product_data.get('update')
            quantity = product_data.get('quantity')
            cart.add(product, quantity=quantity, size_id=size_id, update=update)

        json_response = {'success': True, 'product_quantity': len(cart)}
        return JsonResponse(json_response)
    return JsonResponse({'success': False})


def api_get_cart_items(request):
    cart = Cart(request)
    return JsonResponse(json.dumps(list(cart)), safe=False)


def remove_cart_item(request):
    if request.method == 'POST':
        
        data = json.loads(request.body)
        # print(data)
        cart = Cart(request)
        product = get_object_or_404(Product, pk=data['id'])
        cart.remove(product)
        total = cart.get_total() or 0
        json_response = {
            'total': total,
            'subtotal': total,
        }
        return JsonResponse(json_response)
    
    return JsonResponse({'success': False})


def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart = Cart(request)
        total = cart.get_total()
        if total is None:
            total = 0
        return JsonResponse({'total': total})
