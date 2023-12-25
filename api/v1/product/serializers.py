from rest_framework import serializers
from main import settings

from product.manager import CartSession
from product.models import Item, Order


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CartSessionSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True, source='items')

    class Meta:
        model = CartSession
        fields = '__all__'
