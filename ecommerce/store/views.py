from django.shortcuts import render
from .models import *
from .utils import cartData, guestOrder
from django.http import JsonResponse
import json
import datetime

def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]

    products = Product.objects.all()

    context = {"products": products, "cartItems": cartItems}
    return render(request, "store/store.html", context)

def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "store/cart.html", context)

def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
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


def get_cart_items(request, cart={}):
    items = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.get_cart_items
    else:
        for i in cart:
            items += cart[i]["quantity"]

    return items

def processOrder(request):
    data = json.loads(request.body)
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request)

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