from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class BusCompany(models.Model):
    """Represents a bus company that operates routes and buses."""

    name = models.CharField(max_length=100, unique=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    logo_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    """Represents a travel route between two locations."""

    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("origin", "destination")
        ordering = ["origin", "destination"]

    def __str__(self) -> str:
        return f"{self.origin} → {self.destination}"


class Bus(models.Model):
    """A physical bus belonging to a company."""

    STANDARD = "standard"
    VIP = "vip"
    BUSINESS = "business"

    BUS_TYPE_CHOICES = [
        (STANDARD, "Standard"),
        (VIP, "VIP"),
        (BUSINESS, "Business"),
    ]

    company = models.ForeignKey(BusCompany, on_delete=models.CASCADE, related_name="buses")
    bus_number = models.CharField(max_length=50)
    capacity = models.PositiveIntegerField()
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES, default=STANDARD)
    amenities = models.CharField(max_length=255, blank=True, help_text="Comma-separated list, e.g. WiFi,AC,Charging")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("company", "bus_number")
        ordering = ["company__name", "bus_number"]
        verbose_name = "Bus"
        verbose_name_plural = "Buses"

    def __str__(self) -> str:
        return f"{self.company.name} - {self.bus_number}"


class Schedule(models.Model):
    """A scheduled departure for a given route and bus."""

    ACTIVE = "active"
    INACTIVE = "inactive"

    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    ]

    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="schedules")
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name="schedules")
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["departure_time"]
        indexes = [
            models.Index(fields=["route", "departure_time"]),
        ]

    def __str__(self) -> str:
        return f"{self.route} - {self.departure_time:%Y-%m-%d %H:%M} ({self.bus})"


class Seat(models.Model):
    """Represents a single seat on a scheduled bus trip."""

    AVAILABLE = "available"
    RESERVED = "reserved"
    BOOKED = "booked"

    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (RESERVED, "Reserved"),
        (BOOKED, "Booked"),
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AVAILABLE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("schedule", "seat_number")
        ordering = ["schedule", "seat_number"]

    def __str__(self) -> str:
        return f"{self.schedule} - Seat {self.seat_number} ({self.status})"


class Booking(models.Model):
    """Represents a booking made by a user for a schedule and specific seats."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="bookings")
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT, related_name="bookings")
    seats = models.ManyToManyField(Seat, related_name="bookings")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=CONFIRMED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        seats = ", ".join(self.seats.values_list("seat_number", flat=True))
        return f"Booking #{self.id} by {self.user} for {self.schedule} [{seats}]"

    @property
    def departure_date(self):
        return timezone.localtime(self.schedule.departure_time).date()
