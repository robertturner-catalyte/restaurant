from rest_framework import viewsets, status as http_status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MenuItem, Order, OrderItem
from django.utils import timezone
from .serializers import (
    MenuItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
)


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        active_param = self.request.query_params.get("active")

        if active_param is not None:
            if active_param.lower() =="true":
                qs = qs.filter(active = True)
            elif active_param.lower()== "false":
                qs = qs.filter(active = False)
        return qs
    
    @action(detail=False, methods=["get"], url_path="active")
    def list_active(self, request):
        qs = self.get_queryset().filter(active=True)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=http_status.HTTP_200_OK)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status_param = self.request.query_params.get("status")
        order_type = self.request.query_params.get("order_type")

        if status_param:
            qs = qs.filter(status=status_param)
        if order_type:
            qs = qs.filter(order_type=order_type)
        return qs

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")

        allowed_status = {"new", "in_progress", "completed", "cancelled"}
        if new_status not in allowed_status:
            return Response(
                {"detail": "Invalid status."},
                status = http_status.HTTP_400_BAD_REQUEST,
            )
        if order.status in {"completed", "cancelled"}:
            return Response(
                {"detail": "Completed/Cancelled orders cannot be changed."},
                status = http_status.HTTP_400_BAD_REQUEST,
            )
        order.status = new_status
        if new_status == "completed" and order.picked_up_at is None:
            order.picked_up_at = timezone.now()
        order.save()
        return Response(OrderSerializer(order).data, status=http_status.HTTP_200_OK)
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
