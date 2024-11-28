from django.shortcuts import render, get_object_or_404, redirect

from .cart import Cart
from main.models import Product

from django.http import JsonResponse


def cart_summary(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    total_quantity = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, product_id=product_id)
        cart_items.append({'product': product, 'quantity': quantity})
        total_price += product.price * quantity
        total_quantity += quantity

    return render(request, 'cart_summary.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_quantity': total_quantity,
    })
def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(Product, product_id=product_id)
            cart = request.session.get('cart', {})
            if product_id in cart:
                cart[product_id] += 1  # Increase the quantity
            else:
                cart[product_id] = 1  # Add product with quantity 1
            request.session['cart'] = cart
        return redirect('cart:cart_summary')
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

def cart_update(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})

        # Retrieve the new quantity from the POST request
        new_quantity = int(request.POST.get('quantity', 0))
        product_id_str = str(product_id)  # Convert product_id to string

        # Update or remove the product in the cart
        if new_quantity > 0:
            cart[product_id_str] = new_quantity
        else:
            cart.pop(product_id_str, None)  # Remove the product if quantity is 0 or less

        request.session['cart'] = cart  # Save the updated cart in the session
        return redirect('cart:cart_summary')  # Redirect to the cart summary
    else:
        return redirect('cart:cart_summary')

def store_view(request):
    # Add logic to render a template or perform some action
    return render(request, 'cart/store.html', {})