from django_filters import rest_framework as filters

from rest_framework import viewsets

from store.filters import OrderFilter
from store.models import Book, Order
from store.serializers import BookSerializer, OrderSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer


class OrderViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = OrderFilter
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
