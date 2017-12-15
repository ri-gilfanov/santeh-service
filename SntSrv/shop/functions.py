def move_in_shopping_cart(request):
    if 'product_pk_for_shopping_cart' in request.POST:
        request.session.set_expiry(259200)
        if 'shopping_cart' not in request.session:
            request.session['shopping_cart'] = {}
        product_pk = request.POST['product_pk_for_shopping_cart']
        if product_pk in request.session['shopping_cart'].keys():
            request.session['shopping_cart'].pop(product_pk)
        else:
            if ('product_count_for_shopping_cart' in request.POST
                and request.POST['product_count_for_shopping_cart'].isdigit()
            ):
                product_count = int(request.POST['product_count_for_shopping_cart'])
            else:
                product_count = 1
            request.session['shopping_cart'][product_pk] = product_count
