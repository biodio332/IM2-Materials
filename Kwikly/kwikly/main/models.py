from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class CustomerManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        if not email:
            raise ValueError("The Email field is required")
        
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    customer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True, null=False)  # Changed to CharField with unique=True
    password = models.CharField(max_length=128, default=make_password('temp_password'))
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='customer_profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='store_images/', null=True, blank=True)  # Add image field
    description = models.TextField(null=True, blank=True)  # Add description field
    
    def __str__(self):
        return self.store_name



class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)  # Changed `type` to `name` for clarity
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.type


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL) # Link to Store
    price = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)  # Product price at this store
    image = models.ImageField(upload_to='uploads/products/', default='uploads/products/default.jpg')
    
    def __str__(self):
        return self.store.store_name if self.store else "No Store"



# Order Model
class Order(models.Model):
        order_id = models.AutoField(primary_key=True)
        customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', null=True)
        store = models.ForeignKey(Store, null=True, on_delete=models.SET_NULL)
        total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # New field

        completed = models.BooleanField(default=False)

        def __str__(self):
            return f"Order {self.order_id}"

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=1)

    def __str__(self):
        return f"Order {self.order.order_id} - Product {self.product.product_name} (Quantity: {self.quantity})"

# Transaction Model
class Transaction(models.Model):
    TRANSACTION_STATUS = [
        ('Received', 'Received'),
        ('On Delivery', 'On Delivery'),
        ('Completed', 'Completed'),
        ('Store Received', 'Store Received'),
    ]
    transaction_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Online', 'Online')])
    province = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100,null=True)
    ward = models.CharField(max_length=100,null=True)   
    description = models.TextField(blank=True, null=True)  # Allow optional description
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=TRANSACTION_STATUS, default='Waiting for Store to Receive')
    
    def __str__(self):
        return (
            f"Transaction {self.transaction_id} by {self.customer.username} "
            f"in {self.province}, {self.city}, {self.ward} - {self.description or 'No description'}"
        )
    
