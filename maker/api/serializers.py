from rest_framework import serializers

from maker.models import CryptoCurrency, Metric

#Added by Zou
from maker.models import User, RelatedNews, Log, Timeslot
class CryptoCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoCurrency
        fields = ('id', 'name', 'logo', 'time')     # in doubt: time ok?

class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ('id', 'crypto_currency', 'timeslot', 'volume', 'privacy', 'price', 'supply', 'utility')
        # fields = '__all__'

#Begin ---Zou
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'gender','password', 'interest_tag', 'score_of_knowledge', 'favorite')

class RelatedNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelatedNews
        fields = ('id', 'tag', 'ttype', 'picture', 'content', 'author')

class TimeslotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeslot
        fields = ('id', 'time', 'related_news')

class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Log
        fields = ('id', 'ip', 'time', 'user', 'related_news')

#End-----Zou
