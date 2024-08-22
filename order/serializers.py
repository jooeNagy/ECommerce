from rest_framework import serializers
from . models import *


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(method_name='order_items', read_only=True)
    class Meta:
        model = Order
        fields = '__all__'


    def order_items(self, obj):
        order_items = obj.orderItems.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data