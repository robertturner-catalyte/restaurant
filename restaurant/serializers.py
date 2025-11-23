from rest_framework import serializers
from .models import MenuItem, Order, OrderItem
from rest_framework.exceptions import ValidationError

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ["id", "name", "category", "price", "active"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "menu_item", "quantity", "item_price", "note"]
        read_only_fields = ["id", "item_price"]
        


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", "order_type", "customer_name", "total_amount", "status", "created_at", "updated_at", "picked_up_at", "items"]
        read_only_fields = ["id", "total_amount", "status", "created_at", "updated_at", "picked_up_at"]

    def create(self, validated_data):
        """
        Create an Order and its OrderItems from nested 'items' data.
        Calculates total_amount based on MenuItem.price * quantity.
        """
        items_data = validated_data.pop("items", [])

        if not items_data:
            raise ValidationError({"items": ["At least one item is required."]})
        
        order = Order.objects.create(**validated_data)
        total = 0.0

        for item_data in items_data:
            menu_item = item_data["menu_item"]
            quantity = item_data["quantity"]
            note = item_data.get("note", "")

            if not menu_item.active:
                raise ValidationError({"items": [f"Menu item '{menu_item.name}' is not active"]})

            item_price = menu_item.price

            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=quantity,
                item_price=item_price,
                note=note,
            )

            total += item_price * quantity

        order.total_amount = total
        order.save()

        return order
