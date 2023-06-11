from rest_framework import serializers

from store.models import Book, Order, OrderItem


class BookSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'quantity', 'description']

    def get_quantity(self, obj):
        return obj.bookitem_set.count()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user_email', 'status', 'delivery_address', 'order_id_in_shop', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
