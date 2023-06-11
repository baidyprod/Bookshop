from django_filters import rest_framework as filters

from store.models import Order


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ['status']
