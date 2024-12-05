from django.shortcuts import render, get_object_or_404, redirect
from main.models import Product, Order, OrderProduct
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

app_name = 'cart'

@login_required
def cart_summary(request, store_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Get the active order for the selected store
    order = Order.objects.filter(customer=request.user, store_id=store_id, completed=False).first()

    if not order:
        print("No active order for this store.")  # Debugging output
        cart_items = []  # No active order for the store
        total_quantity = 0
        total_price = 0
        store = None
    else:
        print(f"Order ID: {order.order_id}")  # Debugging output
        # Fetch related OrderProduct items
        cart_items = OrderProduct.objects.filter(order=order)
        # Calculate total quantity and price
        total_quantity = sum(item.quantity for item in cart_items)
        total_price = sum(item.quantity * item.product.price for item in cart_items)
        store = order.store

        # Update and save the total price in the Order instance
        order.total_price = total_price
        order.save()

    context = {
        'cart_items': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price,
        'store': store,
        'order_id': order.order_id if order else None,  # Pass order_id explicitly
        'store_id': store_id,  # Optional if needed
    }

    return render(request, 'cart_summary.html', context)



def cart_add(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, product_id=product_id)

        # Get or create the active cart for the current store
        cart, _ = Order.objects.get_or_create(
            customer=request.user,
            store=product.store,
            completed=False
        )

        # Get or create the order product
        order_product, created = OrderProduct.objects.get_or_create(
            order=cart,
            product=product
        )
        if not created:
            order_product.quantity += quantity
        else:
            order_product.quantity = quantity
        order_product.save()

    return redirect('cart:cart_summary', store_id=product.store.store_id)


def cart_delete(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    cart = Order.objects.filter(customer=request.user, completed=False, store=product.store).first()

    if cart:
        OrderProduct.objects.filter(order=cart, product=product).delete()

    # Redirect with the `store_id` of the product's store
    return redirect('cart:cart_summary', store_id=product.store.store_id)


def cart_update(request, product_id):
    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, product_id=product_id)
        cart = Order.objects.filter(customer=request.user, completed=False, store=product.store).first()

        if cart:
            order_product = OrderProduct.objects.filter(order=cart, product=product).first()
            if order_product:
                if new_quantity > 0:
                    order_product.quantity = new_quantity
                    order_product.save()
                else:
                    order_product.delete()  # Remove the product if quantity is 0

        # Redirect with the `store_id` of the product's store
        return redirect('cart:cart_summary', store_id=product.store.store_id)


def transaction_form(request):
    # Add your logic for handling the transaction form
    return render(request, 'main/templates/transaction_form.html')

def complete_order(request, order_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

 
    # Redirect to the transaction form with the order_id
    return redirect(reverse('main:transaction_form') + f'?order_id={order_id}')


@login_required
def reset_order_status(request, order_id):
    if request.method == 'POST':  # Ensure the action only happens with a POST request
        try:
            # Fetch the order and   validate it belongs to the current user
            order = get_object_or_404(Order, pk=order_id, customer=request.user)
            order.completed = False  # Reset the `completed` attribute
            order.save()
            return redirect('cart:cart_summary', store_id=order.store.store_id)  # Redirect to the cart
        except ValueError:
            return HttpResponseBadRequest("Invalid Order ID.")
    return HttpResponseBadRequest("Invalid request method.")