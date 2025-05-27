$(function() {
    $(document).on('click', '.cart-ops', function() {
        var productId = $(this).data('product')
        var action = $(this).data('action')
        console.log('productId:', productId, 'action:', action)
        if(user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
});

function updateUserOrder(productId, action) {
    console.log('User is authenticated.')
    $.ajax({
        context: this,
        type: "post",
        headers: {"X-CSRFToken": csrftoken},
        url: '/update_item',
        dataType: "json",
        data: JSON.stringify({
            'productId': productId,
            'action': action
        }),
        success: function(data) {
            if(data.status) {
                console.log('Data:', data.cart_items)
                $('#cart-total').text(data.cart_items)
                location.reload()
            } else {
                console.log('Data:', data)
            }
        },
        error: function(data) {
            console.log('Data:', data)
        }
    });
}

function addCookieItem(productId, action) {
    console.log('User is not authenticated.')

    if(action == 'add') {
        if(cart[productId] == undefined) {
            cart[productId] = {'quantity' : 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if(action == 'remove') {
        cart[productId]['quantity'] -= 1

        if(cart[productId]['quantity'] <= 0) {
            delete cart[productId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
    console.log('Cart', cart)
}
