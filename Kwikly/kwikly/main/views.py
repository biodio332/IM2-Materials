# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from django.http import Http404
from .models import Product, Category, Customer, Store,Transaction,Order,OrderProduct

def home(request):
    search_query = request.GET.get('search', None)
    sort_option = request.GET.get('sort', None)
    selected_category = request.GET.get('category', None)
    
    products = Product.objects.all()
    
    if selected_category:
        products = products.filter(category__type=selected_category)

    if search_query:
        products = products.filter(product_name__icontains=search_query)
    
    if sort_option == 'low_to_high':
        products = products.order_by('price')
    elif sort_option == 'high_to_low':
        products = products.order_by('-price')
    
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'sort_option': sort_option,
        'selected_category': selected_category,
        'search_query': search_query, 
    }
    return render(request, 'home.html', context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_staff and user.is_superuser:
                
                return redirect('admin_dashboard')
            else:

                return redirect("store")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("store")

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        
        if password == confirm_password:
            if not Customer.objects.filter(username=username).exists():
                customer = Customer.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    name=name,
                    contact=contact,
                    address=address
                )
                messages.success(request, "Registration successful. You can now log in.")
                return redirect("login")
            else:
                messages.error(request, "Username already exists.")
        else:
            messages.error(request, "Passwords do not match.")
    return render(request, "register.html")


def account_information(request):
    return render(request, 'account.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password was successfully updated!')
            return redirect('account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:  # Ensure only superusers can access this view
        return redirect("home")  # Redirect non-superusers to home

    # Fetch any relevant admin-specific data
    user_count = Customer.objects.count()
    product_count = Product.objects.count()
    store_count = Store.objects.count()

    context = {
        "user_count": user_count,
        "product_count": product_count,
        "store_count": store_count,
    }
    return render(request, "admin_dashboard.html", context)

# Manage Users
@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return redirect("home")

    users = Customer.objects.exclude(is_superuser=True)  # Exclude superusers from the list
    context = {"users": users}
    return render(request, "manage_users.html", context)

# Manage Products
@login_required
def manage_products(request):
    if not request.user.is_superuser:
        return redirect("home")

    products = Product.objects.all()
    context = {"products": products}
    return render(request, "manage_products.html", context)

# Manage Stores
@login_required
def manage_stores(request):
    if not request.user.is_superuser:
        return redirect("home")

    stores = Store.objects.all()
    context = {"stores": stores}
    return render(request, "manage_stores.html", context)

# Add User View
@login_required
def add_user(request):
    if not request.user.is_superuser:
        return redirect("home")  # Ensure only superusers can add users

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email') 
        password = request.POST.get('password')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        if password:
            try:
                user = get_user_model().objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    name=name,
                    contact=contact,
                    address=address,
                )
                messages.success(request, f"User {username} created successfully.")
                return redirect('manage_users')  # Redirect to manage users page after success
            except Exception as e:
                messages.error(request, f"Error creating user: {e}")
    return render(request, 'add_user.html')

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(Customer, customer_id=user_id)
    if request.user.is_superuser:
        user = Customer.objects.get(customer_id=user_id)
    elif request.user.customer_id == user_id:
        # If the logged-in user is the same as the one being edited, allow the edit
        user = Customer.objects.get(customer_id=user_id)
    else:
        # Otherwise, prevent access
        return redirect('account_information')
    # Handle form submission
    if request.method == "POST":
        user.name = request.POST.get("name")
        user.email = request.POST.get("email")
        user.contact = request.POST.get("contact")
        user.address = request.POST.get("address")
        user.save()
        messages.success(request, f"User {user.username} updated successfully.")
        return redirect("manage_users")

    context = {"user": user}
    return render(request, "edit_user.html", context)


# Delete User
@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser:
        return redirect("home")

    user = get_object_or_404(Customer, customer_id=user_id)
    user.delete()
    messages.success(request, f"User {user.username} deleted successfully.")
    return redirect("manage_users")

@login_required
def manage_products(request):
    if not request.user.is_superuser:
        return redirect("home")

    # Get all products
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'manage_products.html', context)

# Add Product View
@login_required
def add_product(request):
    if not request.user.is_superuser:
        return redirect("home")  # Ensure only superusers can add products

    categories = Category.objects.all()
    stores = Store.objects.all()

    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        price = request.POST.get('price')
        category_name = request.POST.get('category')  # Receive category name as string
        store_name = request.POST.get('store')  # Receive store name as string
        image = request.FILES.get('image')

        # Debugging: Print the received values
        print(f"Product Name: {product_name}, Price: {price}, Category: {category_name}, Store: {store_name}, Image: {image}")

        # Check if the required fields are provided
        if not product_name or not price or not category_name or not store_name:
            messages.error(request, "All fields are required.")
            return render(request, 'add_product.html', {
                'categories': categories,
                'stores': stores,
                'product_name': product_name,
                'price': price,
                'category_name': category_name,
                'store_name': store_name,
            })

        try:
            # Look up category by name
            category = Category.objects.get(type=category_name)

            # Look up store by name
            store = Store.objects.get(store_name=store_name)

            # Create a new product and save it
            product = Product(
                product_name=product_name,
                price=price,
                category=category,
                store=store,
                image=image if image else None
            )
            product.save()

            messages.success(request, f"Product '{product_name}' created successfully.")
            return redirect('manage_products')  # Redirect to manage products page after success

        except Category.DoesNotExist:
            messages.error(request, "Category not found.")
        except Store.DoesNotExist:
            messages.error(request, "Store not found.")
        except Exception as e:
            messages.error(request, f"Error creating product: {e}")

    context = {
        'categories': categories,
        'stores': stores,
    }

    return render(request, 'add_product.html', context)




@login_required
def edit_product(request, product_id):
    if not request.user.is_superuser:
        return redirect("home")

    # Get the product object by its product_id
    product = get_object_or_404(Product, product_id=product_id)
    
    if request.method == "POST":
        # Update product fields with the POST data
        product.product_name = request.POST.get("product_name")
        product.price = request.POST.get("price")
        
        # Update category and store by their respective IDs
        product.category = Category.objects.get(category_id=request.POST.get("category"))
        product.store = Store.objects.get(store_id=request.POST.get("store"))
        
        # Handle image upload if provided
        if request.FILES.get("image"):
            product.image = request.FILES["image"]
        else:
            # If no new image is uploaded, retain the existing image
            product.image = product.image

        # Save the updated product
        product.save()

        messages.success(request, f"Product {product.product_name} updated successfully.")
        return redirect('manage_products')

    # Fetch all categories and stores for the form dropdown
    categories = Category.objects.all()
    stores = Store.objects.all()

    context = {
        'product': product,
        'categories': categories,
        'stores': stores,
    }

    return render(request, 'edit_product.html', context)


@login_required
def delete_product(request, product_id):
    if not request.user.is_superuser:
        return redirect("home")

    product = get_object_or_404(Product, product_id=product_id)
    
    # Debugging the user being deleted
    print(f"Deleting product: {product.product_name}")
    
    product.delete()
    messages.success(request, f"Product {product.product_name} deleted successfully.")
    return redirect('manage_products')

@login_required
def manage_stores(request):
    if not request.user.is_superuser:
        return redirect("home")

    stores = Store.objects.all()  # Fetch all stores
    context = {
        'stores': stores,
    }
    return render(request, 'manage_stores.html', context)

@login_required
def add_store(request):
    if not request.user.is_superuser:
        return redirect("home")

    if request.method == "POST":
        store_name = request.POST.get("store_name")
        address = request.POST.get("address")
        description = request.POST.get("description")
        image = request.FILES.get("image")  # Handle the uploaded image file

        # Create new store
        store = Store.objects.create(
            store_name=store_name,
            address=address,
            description=description,
            image=image  # Save the uploaded image
        )

        messages.success(request, f"Store {store.store_name} added successfully.")
        return redirect('manage_stores')

    return render(request, 'add_store.html')

@login_required
def edit_store(request, store_id):
    if not request.user.is_superuser:
        return redirect("home")

    store = get_object_or_404(Store, store_id=store_id)

    if request.method == "POST":
        store.store_name = request.POST.get("store_name")
        store.address = request.POST.get("address")
        store.save()

        messages.success(request, f"Store {store.store_name} updated successfully.")
        return redirect('manage_stores')

    context = {
        'store': store,
    }

    return render(request, 'edit_store.html', context)

@login_required
def delete_store(request, store_id):
    if not request.user.is_superuser:
        return redirect("home")

    store = get_object_or_404(Store, store_id=store_id)
    store_name = store.store_name

    store.delete()

    messages.success(request, f"Store {store_name} deleted successfully.")
    return redirect('manage_stores')

def store_view(request):
    categories = Category.objects.all()  # Fetch categories from the database
    stores = Store.objects.all()          # Fetch stores from the database
    return render(request, 'store.html', {'categories': categories, 'stores': stores})

def store_detail(request, store_id):
    store = get_object_or_404(Store, pk=store_id)
    products = Product.objects.filter(store=store)
    categories = Category.objects.all()  # Fetch categories here

    context = {
        'store': store,
        'products': products,
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'home.html', context)

def cart_summary(request):
    # Your code to render the cart summary
    return render(request, 'cart_summary.html')

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_detail.html', {'product': product})


def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity")
        print(f"Received POST data: product_id={product_id}, quantity={quantity}")  # Debugging

        try:
            quantity = int(quantity)
            if quantity < 1:
                quantity = 1
        except (ValueError, TypeError):
            quantity = 1

        print(f"Processed quantity: {quantity}")  # Debugging

        product = get_object_or_404(Product, pk=product_id)
        cart = Cart(request)
        cart.add(product, quantity)

        print(f"Cart after addition: {cart.cart}") 

        messages.success(request, f"{quantity} x {product.product_name} added to your cart!")
        return redirect("cart:cart_summary")
    
def transaction_form(request):
    return render(request, 'transaction_form.html')


@login_required
def transaction_form(request):
    confirmation_message = False
    customer = request.user

    # Fetch order_id from query string
    order_id = request.GET.get('order_id')

    # Validate order_id
    if not order_id:
        return HttpResponseBadRequest("Order ID is required.")

    try:
        # Ensure order_id is a valid integer and belongs to the user
        order = get_object_or_404(Order, pk=int(order_id), customer=customer)
        
    except ValueError:
        return HttpResponseBadRequest("Invalid Order ID.")

    if request.method == 'POST':
        # Fetch form data
        province = request.POST.get('province')
        city = request.POST.get('city')
        ward = request.POST.get('ward')
        description = request.POST.get('description', '')
        payment_method = request.POST.get('payment_method')

        if not province or not city or not ward or not payment_method:
            return HttpResponseBadRequest("All fields are required.")
        order.completed = True
        order.save()
        # Create a new transaction
        Transaction.objects.create(
            customer=customer,
            order=order,
            payment_method=payment_method,
            province=province,
            city=city,
            ward=ward,
            description=description
        )
        confirmation_message = True



    # Pass the order to the template
    return render(request, 'transaction_form.html', {
    'confirmation_message': confirmation_message,
    'order': order,
    'order_id': order_id,  # Ensure this is included in the context
    
})


# Orders
def add_order(request):
    if request.method == 'POST':
        customer_id = request.POST['customer']
        total_amount = request.POST['total_amount']
        customer = get_object_or_404(Customer, id=customer_id)
        Order.objects.create(customer=customer, total_amount=total_amount)
        return redirect('manage_orders')
    customers = Customer.objects.all()
    return render(request, 'add_order.html', {'customers': customers})

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        customer_id = request.POST['customer']
        total_amount = request.POST['total_amount']
        customer = get_object_or_404(Customer, id=customer_id)
        order.customer = customer
        order.total_amount = total_amount
        order.save()
        return redirect('manage_orders')
    customers = Customer.objects.all()
    return render(request, 'edit_order.html', {'order': order, 'customers': customers})

# Order Products
def add_order_product(request, order_id):
    if request.method == 'POST':
        product_id = request.POST['product']
        quantity = request.POST['quantity']
        price = request.POST['price']
        product = get_object_or_404(Product, id=product_id)
        order = get_object_or_404(Order, id=order_id)
        OrderProduct.objects.create(order=order, product=product, quantity=quantity, price=price)
        return redirect(reverse('view_order', args=[order_id]))
    products = Product.objects.all()
    return render(request, 'add_order_product.html', {'products': products, 'order_id': order_id})

def edit_order_product(request, order_id, order_product_id):
    order_product = get_object_or_404(OrderProduct, id=order_product_id)
    if request.method == 'POST':
        product_id = request.POST['product']
        quantity = request.POST['quantity']
        price = request.POST['price']
        product = get_object_or_404(Product, id=product_id)
        order_product.product = product
        order_product.quantity = quantity
        order_product.price = price
        order_product.save()
        return redirect(reverse('view_order', args=[order_id]))
    products = Product.objects.all()
    return render(request, 'edit_order_product.html', {'order_product': order_product, 'products': products, 'order_id': order_id})

# Transactions
def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)  # Use transaction_id here
    if request.method == 'POST':
        transaction.status = request.POST['status']
        transaction.save()
        return redirect('manage_transactions')
    return render(request, 'edit_transaction.html', {'transaction': transaction})

# Categories
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.type = request.POST['type']
        category.save()
        return redirect('manage_categories')
    return render(request, 'edit_category.html', {'category': category})
    

# View for managing orders
@login_required
def manage_orders(request):
    # Retrieve all orders
    orders = Order.objects.select_related('customer', 'store').order_by('-order_id')
    context = {'orders': orders}
    return render(request, 'manage_orders.html', context)

@login_required
def view_order(request, order_id):
    # Fetch order and its associated products
    order = get_object_or_404(Order, pk=order_id)
    order_products = OrderProduct.objects.filter(order=order).select_related('product')
    context = {
        'order': order,
        'order_products': order_products,
    }
    return render(request, 'view_order.html', context)

@login_required
def delete_order(request, order_id):
    # Delete an order
    order = get_object_or_404(Order, pk=order_id)
    order.delete()
    messages.success(request, f"Order {order_id} has been successfully deleted.")
    return redirect('manage_orders')

# View for managing transactions
def manage_transactions(request):
    # Logic to retrieve and render transaction data
    return render(request, 'manage_transactions.html')

def manage_categories(request):
    """
    View to display all categories and manage them.
    """
    categories = Category.objects.all()
    return render(request, 'manage_categories.html', {'categories': categories})

def add_category(request):
    """
    View to add a new category.
    """
    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_image = request.FILES.get('image')  # Optional image upload

        if category_name:
            Category.objects.create(type=category_name, image=category_image)
            return redirect('manage_categories')
        else:
            return HttpResponse("Category name is required", status=400)

    return render(request, 'add_category.html')

def edit_category(request, category_id):
    """
    View to edit an existing category.
    """
    category = get_object_or_404(Category, category_id=category_id)

    if request.method == 'POST':
        category_name = request.POST.get('name')
        category_image = request.FILES.get('image')  # Optional image upload

        if category_name:
            category.type = category_name
            if category_image:
                category.image = category_image
            category.save()
            return redirect('manage_categories')
        else:
            return HttpResponse("Category name is required", status=400)

    return render(request, 'edit_category.html', {'category': category})


def delete_category(request, category_id):
    """
    View to delete a category.
    """
    category = get_object_or_404(Category, category_id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('manage_categories')

    return render(request, 'confirm_delete.html', {'category': category})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id, customer=request.user)
    return render(request, 'order_detail.html', {'order': order})

def add_transaction(request):
    if request.method == "POST":
        # Extract data from the request
        customer_id = request.POST.get('customer')
        order_id = request.POST.get('order')
        payment_method = request.POST.get('payment_method')
        province = request.POST.get('province')
        city = request.POST.get('city')
        ward = request.POST.get('ward')
        description = request.POST.get('description')

        try:
            # Retrieve the related customer and order
            customer = Customer.objects.get(customer_id=customer_id)
            order = Order.objects.get(order_id=order_id)

            # Create a new transaction
            Transaction.objects.create(
                customer=customer,
                order=order,
                payment_method=payment_method,
                province=province,
                city=city,
                ward=ward,
                description=description
            )

            # Redirect and confirm success
            messages.success(request, "Transaction successfully added.")
            return redirect('manage_transactions')

        except Customer.DoesNotExist:
            messages.error(request, "Selected customer does not exist.")
        except Order.DoesNotExist:
            messages.error(request, "Selected order does not exist.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    # Fetch data for dropdown menus
    customers = Customer.objects.all()
    orders = Order.objects.all()

    # Render the template with necessary data
    return render(request, 'add_transaction.html', {
        'customers': customers,
        'orders': orders,
        'payment_methods': ['Cash', 'Card', 'Online'],  # Choices for payment methods
    })

def manage_transactions(request):
    """
    View to manage and display a list of transactions.
    """
    # Fetch all transactions to display
    transactions = Transaction.objects.select_related('customer', 'order').all()

    context = {
        'transactions': transactions,  # List of transactions to render in the template
    }
    
    return render(request, 'manage_transactions.html', context)

def delete_transaction(request, transaction_id):
    """
    View to delete a transaction.
    """
    transaction = get_object_or_404(Transaction, transaction_id=transaction_id)
    transaction.delete()
    messages.success(request, f"Transaction {transaction_id} has been deleted successfully.")
    return redirect('manage_transactions')

@login_required
def update_profile_picture(request):
    """
    Allows users to update their profile picture.
    """
    if request.method == 'POST':
        user = request.user
        profile_picture = request.FILES.get('profile_picture')

        if profile_picture:
            user.profile_picture = profile_picture
            user.save()
            messages.success(request, 'Profile picture updated successfully.')
        else:
            messages.error(request, 'No file selected.')

        return redirect('account')

    return render(request, 'account.html')

@login_required
def view_transactions(request):
    """View to display current and past transactions for the logged-in user."""
    customer = request.user
    transactions = Transaction.objects.filter(customer=customer).order_by('-date')
    context = {'transactions': transactions}
    return render(request, 'transactions.html', context)

@login_required
def reorder_transaction(request, transaction_id):
    """Allows the user to reorder a transaction if it is marked as 'Delivered' or 'Completed'."""
    transaction = Transaction.objects.get(transaction_id=transaction_id, customer=request.user)
    if transaction.status in ['Completed', 'Delivered']:
        # Create a new order for the user, duplicating the products from the original order
        new_order = Order.objects.create(
            customer=request.user,
            store=transaction.order.store,
            total_price=transaction.order.total_price
        )
        
        # Copy products from the original order to the new order
        order_products = OrderProduct.objects.filter(order=transaction.order)
        for item in order_products:
            OrderProduct.objects.create(
                order=new_order,
                product=item.product,
                quantity=item.quantity
            )

        return redirect('view_transactions')
    else:
        return redirect('view_transactions')