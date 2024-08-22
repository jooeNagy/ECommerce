from django.urls import path
from . import views



urlpatterns = [
    path('products', views.all_products),
    path('products/<int:pk>', views.one_product),
    path('products/new', views.new_product),
    path('products/edit/<int:pk>', views.update_product),
    path('products/delete/<int:pk>', views.delete_product),
    path('products/reviews/<int:pk>', views.add_review, name='create_review'),
    path('products/reviews/delete/<int:pk>', views.delete_review, name='delete_review'),
]
