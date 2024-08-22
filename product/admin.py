from django.contrib import admin
# from .models import Product
from . import models

# Register your models here.


admin.site.register(models.Product)
admin.site.register(models.Review)