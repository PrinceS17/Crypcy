from rest_framework import serializers

from maker.models import CryptoCurrency

class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ('id', 'name', 'logo', 'time')     # in doubt: time ok?