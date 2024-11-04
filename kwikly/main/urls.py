from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.user_register, name="register"),
    path('account/', views.account_information, name='account'),
    path('account/change_password/', views.change_password, name='change_password'),
]