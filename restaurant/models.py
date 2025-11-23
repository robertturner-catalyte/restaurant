from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50)
    price = models.FloatField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.category})"
    

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
    ("new", "New"),
    ("in_progess", "In_Progress"),
    ("completed", "Completed"),
    ("cancelled", "Cancelled")
    ]

    ORDER_TYPE_CHOICES = [
    ("pickup", "Picked"),
    ("delivery", "Delivery"),
    ("dine_in", "Dine_In")
    ]

    order_type = models.CharField(max_length=50, choices=ORDER_TYPE_CHOICES)
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.FloatField(default=0.00)
    status = models.CharField(max_length=50, choices=ORDER_STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    picked_up_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} ({self.order_type})"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, related_name="order_items", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    item_price = models.FloatField()
    note = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name} (Order {self.order_id})"