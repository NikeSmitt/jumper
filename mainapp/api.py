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
        
        cart.add(product, quantity=data['quantity'])
        # print(cart)
        
        return JsonResponse(json_response)
    return JsonResponse({'success': False})


def api_get_cart_items(request):
    # if not request.user.is_authenticated:
    cart = Cart(request)
    # print(cart.cart)
    # print(list(cart))
    # context = {
    #     'cart': cart
    # }
    return JsonResponse(json.dumps(list(cart)), safe=False)


def remove_cart_item(request):
    if request.method == 'POST':
        json_response = {'success': True}
        data = json.loads(request.body)
        cart = Cart(request)
        product = get_object_or_404(Product, pk=data['id'])
