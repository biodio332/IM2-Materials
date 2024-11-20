from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import datetime
# Create your models here.


# Custom User Manager
class CustomerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

<<<<<<< Updated upstream:kwikly/main/models.py
class Customer(AbstractBaseUser):
=======
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, password, **extra_fields)


# Customer Model
class Customer(AbstractBaseUser, PermissionsMixin):
>>>>>>> Stashed changes:Kwikly/kwikly/main/models.py
    customer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128,default=make_password('temp_password'))  # Handled by AbstractBaseUser for secure hashing
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=15, blank=True)  # Restricting length for valid phone numbers
    address = models.TextField(blank=True, null=True)  # Allow multiline addresses
    is_active = models.BooleanField(default=True)
<<<<<<< Updated upstream:kwikly/main/models.py
=======
    is_staff = models.BooleanField(default=False)
>>>>>>> Stashed changes:Kwikly/kwikly/main/models.py

    objects = CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


# Store Model
class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
<<<<<<< Updated upstream:kwikly/main/models.py
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='store_images/', null=True, blank=True)  # Add image field
    description = models.TextField(null=True, blank=True)  # Add description field

=======
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='store_images/', null=True, blank=True)  # Add image field
    description = models.TextField(null=True, blank=True)  # Add description field
    
>>>>>>> Stashed changes:Kwikly/kwikly/main/models.py
    def __str__(self):
        return self.store_name


# Category Model
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
<<<<<<< Updated upstream:kwikly/main/models.py
    type = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    
=======
    type = models.CharField(max_length=255)  # Changed `type` to `name` for clarity
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

>>>>>>> Stashed changes:Kwikly/kwikly/main/models.py
    def __str__(self):
        return self.type


# Product Model
class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
<<<<<<< Updated upstream:kwikly/main/models.py
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # New field for product image

    def __str__(self):
        return self.product_name
=======
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products', default=1)  # Product belongs to a specific store
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='uploads/products/', default='uploads/products/default.jpg')
>>>>>>> Stashed changes:Kwikly/kwikly/main/models.py

    def __str__(self):
        return f"{self.product_name} - {self.store.store_name}"


# Transaction Model
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.CharField(max_length=50, choices=[('Cash', 'Cash'), ('Card', 'Card'), ('Online', 'Online')])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.transaction_id} by {self.customer.username}"


# Order Model
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='orders')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - Store: {self.store.store_name}"


# OrderProduct Model
class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.PositiveIntegerField()

    def __str__(self):
<<<<<<< Updated upstream:kwikly/main/models.py
        return f"Order {self.order.order_id} - Product {self.product.product_name} (Quantity: {self.quantity})"


=======
        return f"Order {self.order.order_id} - {self.product.product_name} (Qty: {self.quantity})"
    
def add_to_cart(request, product_id):
    # Logic for adding the product to the cart
    product = Product.objects.get(id=product_id)
    # Add to cart logic (e.g., using session or a Cart model)
    return redirect('cart_summary')
>>>>>>> Stashed changes:Kwikly/kwikly/main/models.py
