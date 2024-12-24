from django.db import models
from db_connection import db


# Create your models here.
class Order(models.Model):
    pickupLocation = models.CharField(max_length=255)
    dropOffLocation = models.CharField(max_length=255)
    details = models.CharField(max_length=255)
    deliveryTime = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    userId = models.CharField(max_length=255)
    courierId = models.CharField(max_length=255)


Order_collection = db['Order']
