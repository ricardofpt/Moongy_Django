$(function() {
    $(document).on('click', '.cart-ops', function() {
        var productId = $(this).data('product')
        var action = $(this).data('action')
        console.log('productId:', productId, 'action:', action)
    })
});