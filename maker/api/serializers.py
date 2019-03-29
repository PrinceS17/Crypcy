from rest_framework import serializers

from maker.models import CryptoCurrency, Metric

class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ('id', 'name', 'logo', 'time')     # in doubt: time ok?

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('id', 'crypto_currency', 'timeslot', 'volume', 'privacy', 'price', 'supply', 'utility')
        # fields = '__all__'
