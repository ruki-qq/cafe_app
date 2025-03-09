from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import ItemViewSet, OrderViewSet

v1_router = DefaultRouter()
v1_router.register("items", ItemViewSet, basename="item")
v1_router.register("orders", OrderViewSet, basename="order")

urlpatterns = [
    path("", include(v1_router.urls)),
]
