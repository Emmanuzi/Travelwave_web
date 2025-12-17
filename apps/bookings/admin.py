from django.contrib import admin
from .models import BusCompany, Route, Bus, Schedule, Seat, Booking


@admin.register(BusCompany)
class BusCompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "contact_email", "contact_phone")
    search_fields = ("name", "contact_email", "contact_phone")


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("origin", "destination", "distance_km", "duration_minutes")
    list_filter = ("origin", "destination")
    search_fields = ("origin", "destination")


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("bus_number", "company", "capacity", "bus_type")
    list_filter = ("company", "bus_type")
    search_fields = ("bus_number", "company__name")


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("route", "bus", "departure_time", "arrival_time", "price", "status")
    list_filter = ("status", "route__origin", "route__destination", "bus__company")
    search_fields = ("route__origin", "route__destination", "bus__bus_number")
    date_hierarchy = "departure_time"


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("schedule", "seat_number", "status")
    list_filter = ("status", "schedule__route__origin", "schedule__route__destination")
    search_fields = ("seat_number",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "schedule", "total_price", "status", "created_at")
    list_filter = ("status", "schedule__route__origin", "schedule__route__destination")
    search_fields = ("user__username", "schedule__route__origin", "schedule__route__destination")
    date_hierarchy = "created_at"
