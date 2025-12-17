from django.db import models


class Parcel(models.Model):
    """Simple parcel model for Phase 1 tracking demo."""

    STATUS_RECEIVED = "received"
    STATUS_IN_TRANSIT = "in_transit"
    STATUS_OUT_FOR_DELIVERY = "out_for_delivery"
    STATUS_DELIVERED = "delivered"

    STATUS_CHOICES = [
        (STATUS_RECEIVED, "Received"),
        (STATUS_IN_TRANSIT, "In Transit"),
        (STATUS_OUT_FOR_DELIVERY, "Out for Delivery"),
        (STATUS_DELIVERED, "Delivered"),
    ]

    tracking_number = models.CharField(max_length=50, unique=True)
    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_RECEIVED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.tracking_number} ({self.get_status_display()})"
