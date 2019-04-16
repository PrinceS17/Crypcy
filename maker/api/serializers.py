from rest_framework import serializers

from maker.models import CryptoCurrency, Metric, RelatedNews

class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ('id', 'name', 'logo', 'time')     # in doubt: time ok?

class MetricSerializer(serializers.ModelSerializer):
    # crypto_currency = CryptoCurrencySerializer(read_only=True)
    
    class Meta:
        model = Metric
        fields = ('id', 'timeslot', 'volume', 'privacy', 'price', 'supply', 'utility')
        
        # fields = '__all__'
    
    # name = serializers.SerializerMethodField()

    # def get_name(self, obj):
    #     return obj.crypto_currency.id

class RelatedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedNews
        fields = '__all__'