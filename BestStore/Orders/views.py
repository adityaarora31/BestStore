from itertools import count

from django.shortcuts import render
from Products.models import Product


def checkout(request):
    cart = request.session.get('cart', dict())
    prods = {k: cart_detail_to_product(v) for k, v in cart.items()}
    return render(request, 'Orders/checkout.html', context={'products': prods})


def cart_detail_to_product(prod_dict):
    copy = prod_dict.copy()
    pk = copy.pop('pk')
    copy['product'] = Product.objects.get(pk=pk)
    copy['total_product_price'] = copy['product'].price * copy['qty']
    return copy


def orders(request):
    # if request.method == 'POST':
    #     customer = request.user.username
    #     address = request.POST.get('shipping_address')
    #     data = request.session['cart']
    #     for key, value in data.items():
    #         product_id = value['pk']
    #         product_id = int(product_id)
    #         for value in value['qty']:
    #
    #
    #
    #
    #         import pdb;pdb.set_trace()
        return render(request, 'Orders/orders.html')
    #
