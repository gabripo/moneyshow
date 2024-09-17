from django.db import models


# Create your models here.
class Stock(models.Model):
    ticker = models.CharField(max_length=5)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    last_time_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name
