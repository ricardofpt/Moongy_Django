import json
from .models import *

def guestOrder(request):
    data = json.loads(request.body)
    name = data["form"]["name"]
    email = data["form"]["name"]

    cookieData = cookieCart(request)
    items = cookieData["items"]

    # using the get or create method is cool because this way we know all the orders
    # made by the same guest,
    # and if he actually creates an account we'll have all it's previous orders
    customer, created = Customer.objects.get_or_create(email=email)
    customer.name = name
    customer.save()

    order = Order.objects.create(customer=customer, complete=False)

    for item in items:
        product = Product.objects.get(id=item["product"]["id"])

        orderItem = OrderItem.objects.create(
            product=product, order=order, quantity=item["quantity"]
        )

    return customer, order


def cartData(request):
    if request.user.is_authenticated:
        # get the customer
        customer = request.user.customer
        # get the incomplete order, or create a new one
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        # get the order items
        # we can query child objects by setting the parent value (order) 
        # and the child in lowercase (orderitem)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData["cartItems"]
        order = cookieData["order"]
        items = cookieData["items"]

    return {"items": items, "order": order, 'cartItems': cartItems}

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES["cart"])
    except Exception:
        cart = {}
    items = []
    order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
    cartItems = order["get_cart_items"]

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total = product.price * cart[i]["quantity"]

            order["get_cart_total"] += total
            order["get_cart_items"] += cart[i]["quantity"]

            item = {
                "product": {
                    "id": i,
                    "name": product.name,
                    "price": product.price,
                    "image_url": product.image,
                },
                "quantity": cart[i]["quantity"],
                "get_total": total,
            }

            items.append(item)

            if product.digital is False:
                order["shipping"] = True
        except Exception:
            pass

    return {"items": items, "order": order, "cartItems": cartItems}