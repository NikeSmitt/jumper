import json

from django.http import JsonResponse

from cartapp.cart import Cart
from django.shortcuts import get_object_or_404

from mainapp.models.product import Product


def api_add_to_cart(request):
    if request.method == 'POST':
        json_response = {'success': True}
        data = json.loads(request.body)
        cart = Cart(request)
        product = get_object_or_404(Product, pk=data['id'])
        size_id = data.get('size_id')
        cart.add(product, quantity=data['quantity'], size_id=size_id)
        
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
