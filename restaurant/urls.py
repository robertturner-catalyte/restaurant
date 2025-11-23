from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import MenuItemViewSet, OrderViewSet, OrderItemViewSet

router = DefaultRouter()
router.register(r"menu-items", MenuItemViewSet, basename="menuitems")
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"order-items", OrderItemViewSet, basename="orderitems")

urlpatterns = [
    path("", include(router.urls)),
]
