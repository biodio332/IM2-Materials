from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
import datetime
# Create your models here.

class CustomerManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

class Customer(AbstractBaseUser):
    customer_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128,default=make_password('temp_password'))  # Handled by AbstractBaseUser for secure hashing
    name = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.store_name


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return f"Transaction {self.transaction_id}"


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    order_date = models.DateField()

    def __str__(self):
        return f"Order {self.order_id}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)  # New field for product image

    def __str__(self):
        return self.product_name

class OrderProduct(models.Model):
    order_product_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order {self.order.order_id} - Product {self.product.product_name} (Quantity: {self.quantity})"

