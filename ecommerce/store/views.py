from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime

def store(request):
    products = Product.objects.all()
    context = {'products': products, 'cartItems': get_cart_items(request)}
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
            "shipping": False
        }
    context = {"items": items, "order": order, 'cartItems': get_cart_items(request)}
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
            "shipping": False
        }
    context = {"items": items, "order": order, 'cartItems': get_cart_items(request)}
    return render(request, "store/checkout.html", context)

def updateItem(request):
    response = {
        "status": False,
        "msg": '',
        'cart_items': 0
    }
    try:
        data = json.loads(request.body)
        product_id = data["productId"]
        action = data["action"]

        customer = request.user.customer
        product = Product.objects.get(id=product_id)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == "add":
            orderItem.quantity += 1
        if action == "remove":
            orderItem.quantity -= 1

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        response["status"] = True
        response["msg"] = "Item was added"
        response["cart_items"] = order.get_cart_items
    except Exception as e:
        response["msg"] = e

    return JsonResponse(response, safe=False)


def get_cart_items(request):
    items = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.get_cart_items

    return items

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_items:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                state=data["shipping"]["state"],
                zip_code=data["shipping"]["zipcode"],
            )

    return JsonResponse('Payment complete!', safe=False)