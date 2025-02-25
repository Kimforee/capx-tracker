from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stocks', null=True, blank=True)
    name = models.CharField(max_length=255)  # Stock name
    ticker = models.CharField(max_length=10)  # Stock ticker symbol
    quantity = models.PositiveIntegerField(default=1)  # Quantity of stocks
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)  # Buy price per stock
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp of last update

    def __str__(self):
        return f"{self.name} ({self.ticker})"
