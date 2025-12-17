from django.contrib import admin
from .models import Parcel


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ("tracking_number", "sender_name", "receiver_name", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("tracking_number", "sender_name", "receiver_name")
