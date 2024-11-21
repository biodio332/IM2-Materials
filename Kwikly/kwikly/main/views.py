# main/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from .models import Product, Category, Customer, Store

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

                return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("home")

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        
        if password == confirm_password:
            if not Customer.objects.filter(username=username).exists():
                customer = Customer.objects.create_user(
                    username=username,
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
        password = request.POST.get('password')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        if password:
            try:
                user = get_user_model().objects.create_user(
                    username=username,
                    password=password,
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
    if not request.user.is_superuser:
        return redirect("home")

    user = get_object_or_404(Customer, customer_id=user_id)

    # Handle form submission
    if request.method == "POST":
        user.name = request.POST.get("name")
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

        # Create new store
        store = Store.objects.create(
            store_name=store_name,
            address=address,
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


