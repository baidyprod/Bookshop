from django_filters import rest_framework as filters

from rest_framework import viewsets

from store.models import Book, Order
from store.serializers import BookSerializer, OrderSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ['status']


class OrderViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = OrderFilter
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
