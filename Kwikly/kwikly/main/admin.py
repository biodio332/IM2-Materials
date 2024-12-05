from django.contrib import admin
from .models import Customer, Store, Transaction, Order, OrderProduct, Product, Category


admin.site.register(Store)
admin.site.register(Transaction)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Product)
admin.site.register(Category)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'contact', 'address', 'is_active')
    search_fields = ('username',)
    ordering = ('username',)
    
