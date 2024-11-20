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
            if user.is_staff and user.is_superuser:
                
                return redirect('/admin/')
            else:
                
                login(request, user)
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
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                user.save()
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