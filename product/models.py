from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Category(models.TextChoices):
    COMPUTER = 'Computers'
    FOOD = 'Food'
    KIDS = 'Kids'
    HOME = 'Home'


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField(max_length=1000, blank=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    brand = models.CharField(max_length=100, blank=False)
    category = models.CharField(max_length=100, choices=Category.choices)
    rating = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    


class Review(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    ratings = models.IntegerField(default=0)
    comment = models.TextField(max_length=1000, default="", blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)

    def ___str__(self):
        return self.product
    

