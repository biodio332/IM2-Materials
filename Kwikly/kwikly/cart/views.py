from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from main.models import Product

from django.http import JsonResponse


def cart_summary(request):
    # Retrieve cart from session
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    # Loop over the cart items (stored by product_id) and fetch their details
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, product_id=product_id)

        cart_items.append({'product': product, 'quantity': quantity})
        total_price += product.price * quantity

    return render(request, 'cart_summary.html', {'cart_items': cart_items, 'total_price': total_price})

def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            # Get the product object based on the provided product_id
            product = get_object_or_404(Product, product_id=product_id)

            # Retrieve the cart from the session, or initialize an empty cart
            cart = request.session.get('cart', {})

            # If the product is already in the cart, increment its quantity
            if product_id in cart:
                cart[product_id] += 1
            else:
                # Otherwise, add it to the cart with quantity 1
                cart[product_id] = 1

            # Save the cart back to the session
            request.session['cart'] = cart

        # Redirect back to the cart summary page after adding the product
        return redirect('cart:cart_summary')
    else:
        return redirect('cart:cart_summary')

def cart_view(request):
    # Retrieve cart items from the session (or database if using a model-based cart)
    cart = request.session.get('cart', {})

    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(product_id=product_id)
        cart_items.append({'product': product, 'quantity': quantity})
        total_price += product.price * quantity

    return render(request, 'cart_summary.html', {'cart_items': cart_items, 'total_price': total_price})

def cart_delete(request, product_id):
    # Convert product_id to string (as keys in session are strings)
    product_id_str = str(product_id)

    # Retrieve the cart from the session
    cart = request.session.get('cart', {})

    # If the product is in the cart, delete it
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart

    # Redirect back to the cart summary page after deleting the product
    return redirect('cart:cart_summary')

def cart_update(request):
    pass

def store_view(request):
    # Add logic to render a template or perform some action
    return render(request, 'cart/store.html', {})