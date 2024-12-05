from django.urls import path, include
from . import views
from django.urls import include

app_name = 'main'

urlpatterns = [
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
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('transaction_form/', views.transaction_form, name='transaction_form'),
     # Orders
    path('orders/add/', views.add_order, name='add_order'),
    path('orders/edit/<int:order_id>/', views.edit_order, name='edit_order'),
    
    # Order Products
    path('orders/<int:order_id>/products/add/', views.add_order_product, name='add_order_product'),
    path('orders/<int:order_id>/products/edit/<int:order_product_id>/', views.edit_order_product, name='edit_order_product'),

    # Transactions
    path('transactions/edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    
    # Categories
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    # Add the following URLs
    path('manage-orders/', views.manage_orders, name='manage_orders'),
    path('manage-transactions/', views.manage_transactions, name='manage_transactions'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('delete-transaction/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('view_order/<int:order_id>/', views.view_order, name='view_order'),
    path('delete_order/<int:order_id>/', views.delete_order, name='delete_order'),
    path('add-category/', views.add_category, name='add_category'),
    path('manage-categories/', views.manage_categories, name='manage_categories'),
    path('add-category/', views.add_category, name='add_category'),
    path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
]