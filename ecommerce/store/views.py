from django.shortcuts import render
from .models import *

def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, "store/store.html", context)


def cart(request):
    # the store will allow purchases whether the visitor is authenticated or not, 
    # but we have to handle them differently.
    if request.user.is_authenticated:
        # get the customer
        customer = request.user.customer
        # get the incomplete order, or create a new one
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # get the order items
        # we can query child objects by setting the parent value (order) 
        # and the child in lowercase (orderitem)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {  # we need to set this to prevent errors when user is not logged in
            "get_cart_total": 0,
            "get_cart_items": 0,
        }  # we'll handle this later
    context = {"items": items, "order": order}
    return render(request, "store/cart.html", context)


def checkout(request):
    # the store will allow purchases whether the visitor is authenticated or not, 
    # but we have to handle them differently.
    if request.user.is_authenticated:
        # get the customer
        customer = request.user.customer
        # get the incomplete order, or create a new one
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # get the order items
        # we can query child objects by setting the parent value (order) 
        # and the child in lowercase (orderitem)
        items = order.orderitem_set.all()
    else:
        items = []  # we'll handle this later
        order = {  # we need to set this to prevent errors when user is not logged in
            "get_cart_total": 0,
            "get_cart_items": 0,
        }
    context = {"items": items, "order": order}
    return render(request, "store/checkout.html", context)