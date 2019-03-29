from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from maker.models import CryptoCurrency
from .serializers import CryptoCurrencySerializer

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
    permission_classes = (permissions.IsAuthenticated, )    # in doubt: if complicate the use?

class CryptoCurrencyUpdateView(UpdateAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.IsAuthenticated, )    # in doubt: if complicate the use?

class CryptoCurrencyDeleteView(DestroyAPIView):
    queryset = CryptoCurrency.objects.all()
    serializer_class = CryptoCurrencySerializer
    permission_classes = (permissions.IsAuthenticated, )    # in doubt: if complicate the use?