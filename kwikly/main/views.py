# main/views.py
<<<<<<< Updated upstream:kwikly/main/views.py
from django.http import HttpResponse
# main/views.py
from .models import Product, Category, Store
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
=======
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
>>>>>>> Stashed changes:Kwikly/kwikly/main/views.py
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
<<<<<<< Updated upstream:kwikly/main/views.py

=======
from .models import Product, Category, Customer, Store
>>>>>>> Stashed changes:Kwikly/kwikly/main/views.py

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories
    }
    
    return render(request, 'home.html', context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # replace "home" with the name of your home route
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")  # Redirect to login page after logout

def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
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
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change
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
<<<<<<< Updated upstream:kwikly/main/views.py
    store = get_object_or_404(Store, id=store_id)
    return render(request, 'store_detail.html', {'store': store})

#for cart
def cart(request):
    # Your cart view logic here
    return render(request, 'cart.html')
=======
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
    # Your view logic (e.g., pulling cart data from a session or model)
    return render(request, 'cart_summary.html')  # Replace with your actual template
>>>>>>> Stashed changes:Kwikly/kwikly/main/views.py
