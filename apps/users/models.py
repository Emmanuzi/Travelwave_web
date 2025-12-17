from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Extended profile information for a user."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"Profile for {self.user.username}"
