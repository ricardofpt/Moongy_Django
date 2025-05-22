$(function() {
    $(document).on('click', '.cart-ops', function() {
        var productId = $(this).data('product')
        var action = $(this).data('action')
        console.log('productId:', productId, 'action:', action)
        if(user === 'AnonymousUser') {
            console.log('User is not authenticated.')
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
