from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Stock

class StockSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    buy_price = serializers.FloatField()
    class Meta:
        model = Stock
        fields = '__all__'
