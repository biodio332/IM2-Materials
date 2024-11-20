from django.urls import path, include
from . import views
<<<<<<< Updated upstream:kwikly/main/urls.py
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

=======
from django.urls import include
>>>>>>> Stashed changes:Kwikly/kwikly/main/urls.py
urlpatterns = [
    path('', views.store_view, name='store'),
    path('products/',views.home,name='home'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path('account/', views.account_information, name='account'),
<<<<<<< Updated upstream:kwikly/main/urls.py
    path('account/change_password/', views.change_password, name='change_password'),
    path('store/', views.store_view, name='store'), 
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
=======
    path('account/change_password/', views.change_password, name='change_password'), 
    path('store/<int:store_id>/', views.store_detail, name='store_detail'),
    path('cart/',include('cart.urls')),
     path('cart/summary/', views.cart_summary, name='cart_summary'),
>>>>>>> Stashed changes:Kwikly/kwikly/main/urls.py
]