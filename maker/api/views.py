from rest_framework import permissions
from django.http import HttpResponse

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from maker.models import CryptoCurrency, Metric
from .serializers import CryptoCurrencySerializer, MetricSerializer

class CryptoCurrencyListView(ListAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.AllowAny, )

class CryptoCurrencyDetailView(RetrieveAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.AllowAny, )

class CryptoCurrencyCreateView(CreateAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.AllowAny, )    # in doubt: if complicate the use?

class CryptoCurrencyUpdateView(UpdateAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.AllowAny, )    # in doubt: if complicate the use?

class CryptoCurrencyDeleteView(DestroyAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.AllowAny, )    # in doubt: if complicate the use?

class MetricListView(ListAPIView):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    permission_classes = (permissions.AllowAny, )

def test_view(request):
    return HttpResponse("Test view: passed.")