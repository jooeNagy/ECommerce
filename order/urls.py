from django.urls import path
from . import views



urlpatterns = [
    path('orders/new/', views.new_order, name='new_order'),
    path('orders/', views.get_orders, name='get_orders'),
    path('orders/<int:pk>/', views.get_order, name='get_order'),
    path('orders/process/<int:pk>/', views.process_order, name='process_order'),
    path('orders/delete/<int:pk>/', views.delete_order, name='delete_order'),
]
