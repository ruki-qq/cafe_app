from rest_framework import permissions, viewsets

from api.v1.serializers import (
    ItemSerializer,
    ReadOrderSerializer,
    WriteOrderSerializer,
)
from orders.models import Item, ItemQuantity, Order


class ItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = None

    # filter_backends = [DjangoFilterBackend]
    # filterset_class = ItemFilter


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = OrderFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return ReadOrderSerializer
        return WriteOrderSerializer

    def update(self, request, *args, **kwargs):
        return super().update(request, partial=False)
