from django.db import models

# Create your models here.
class BusCompany(models.Model):
    name = models.CharField()

class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

class Schedule(models.Model):
    route = models.CharField()
    price = models.DecimalField()

    