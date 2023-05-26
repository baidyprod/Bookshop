from rest_framework import serializers

from store.models import Book, BookItem, Order, OrderItem, OrderItemBookItem


class BookSerializer(serializers.ModelSerializer):
    quantity = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'price', 'quantity']

    def get_quantity(self, obj):
        return obj.bookitem_set.count()


class BookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookItem
        fields = ['book_id', 'place']


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['user_email', 'status', 'delivery_address', 'order_id_in_shop']


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['order_id', 'book_id', 'quantity']


class OrderItemBookItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItemBookItem
        fields = ['order_item_id', 'book_item_id']
