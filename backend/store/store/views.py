from rest_framework import viewsets

from store.models import Book, BookItem, Order, OrderItem, OrderItemBookItem
from store.serializers import BookItemSerializer, BookSerializer, OrderItemBookItemSerializer, OrderItemSerializer, \
    OrderSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer


class BookItemViewSet(viewsets.ModelViewSet):
    queryset = BookItem.objects.all().order_by('-created_at')
    serializer_class = BookItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all().order_by('-created_at')
    serializer_class = OrderItemSerializer


class OrderItemBookItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItemBookItem.objects.all().order_by('-created_at')
    serializer_class = OrderItemBookItemSerializer
