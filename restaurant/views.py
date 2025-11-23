from rest_framework import viewsets
from .models import MenuItem, Order, OrderItem
from .serializers import MenuItemSerializer, OrderItemSerializer, OrderSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all
    serializer_class = MenuItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all
    serializer_class = OrderSerializer

class OrderItemViewset(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all
    serializer_class = OrderItemSerializer
