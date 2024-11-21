
# kwikly/urls.py
from django.contrib import admin
from django.urls import path
from main import views  # Import the view from the 'main' app
from . import settings
from django.urls import include

from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.store_view, name='store'),
    path('products/',views.home,name='home'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path('account/', views.account_information, name='account'),
    path('account/change_password/', views.change_password, name='change_password'), 
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('cart/',include('cart.urls')),
    path('cart/summary/', views.cart_summary, name='cart_summary'),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('manage_users/', views.manage_users, name='manage_users'),
    path('manage_products/', views.manage_products, name='manage_products'),
    path('manage_stores/', views.manage_stores, name='manage_stores'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('manage_stores/', views.manage_stores, name='manage_stores'),
    path('add_store/', views.add_store, name='add_store'),
    path('edit_store/<int:store_id>/', views.edit_store, name='edit_store'),
    path('delete_store/<int:store_id>/', views.delete_store, name='delete_store'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
