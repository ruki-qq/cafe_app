from django_filters.rest_framework import FilterSet, filters

from orders.models import Order


class OrderFilter(FilterSet):
    """Filter для поиска заказов по статусу."""

    class Meta:
        model = Order
        fields = ["status"]
