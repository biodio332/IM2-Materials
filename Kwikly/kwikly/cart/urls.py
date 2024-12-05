from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
  path('summary/<int:store_id>/', views.cart_summary, name='cart_summary'),
  path('add/', views.cart_add, name='cart_add'),
  path('delete/<int:product_id>/', views.cart_delete, name='cart_delete'),
  path('update/<int:product_id>/', views.cart_update, name='cart_update'),
  path('complete_order/<int:order_id>/', views.complete_order, name='complete_order'),
  path('reset_order/<int:order_id>/', views.reset_order_status, name='reset_order_status'),
]