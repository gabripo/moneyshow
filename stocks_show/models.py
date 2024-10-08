from django.db import models


# Create your models here.
class StockData(models.Model):
    ticker = models.TextField(null=True)
    prices = models.TextField(null=True)
