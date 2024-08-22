from django.db import models
from operator import mod
from django.contrib.auth.models import User
from product.models import Product

# Create your models here.


class OrderStatus(models.TextChoices):
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'


class PaymentStatus(models.TextChoices):
    PAID = 'paid'
    UNPAID = 'unpaid'


class PaymentMode(models.TextChoices):
    COD = 'COD'
    CARD = 'CARD'


class Order(models.Model):
    city = models.CharField(max_length=400, default="", blank=False)
    zip_code = models.CharField(max_length=100, default="", blank=False)
    street = models.CharField(max_length=500, default="", blank=False)
    state = models.CharField(max_length=100, default="", blank=False)
    country = models.CharField(max_length=100, default="", blank=False)
    phone_no = models.CharField(max_length=15, default="", blank=False)
    total_amount = models.IntegerField(default=0)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus, default=PaymentStatus.UNPAID)
    payment_mode = models.CharField(max_length=30, choices=PaymentMode, default=PaymentMode.COD)
    status = models.CharField(max_length=30, choices=OrderStatus, default=OrderStatus.PROCESSING)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
    


class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE, related_name='orderItems')
    name = models.CharField(max_length=200, default="", blank=False)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=3, blank=False)

    def __str__(self):
        return self.name