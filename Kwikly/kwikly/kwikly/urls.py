
# kwikly/urls.py
from django.contrib import admin
from django.urls import path
from main import views  # Import the view from the 'main' app
from . import settings
from django.urls import include

from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  # Map the root URL ('/') to the home view
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path('account/', views.account_information, name='account'),
    path('account/change_password/', views.change_password, name='change_password'),
    path('cart/',include('cart.urls')),
    path('cart/summary/', views.cart_summary, name='cart_summary'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
