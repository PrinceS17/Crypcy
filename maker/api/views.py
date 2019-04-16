# from rest_framework import permissions
# from django.http import HttpResponse
# from django.db import connection
# from maker.sql_operation import dictfetchall


# from rest_framework.generics import (
#     ListAPIView,
#     RetrieveAPIView,
#     CreateAPIView,
#     DestroyAPIView,
#     UpdateAPIView
# )
# from maker.models import CryptoCurrency, Metric
# from .serializers import CryptoCurrencySerializer, MetricSerializer

# class CryptoCurrencyListView(ListAPIView):
#     queryset = CryptoCurrency.objects.all()
#     serializer_class = CryptoCurrencySerializer
#     permission_classes = (permissions.AllowAny, )

# class CryptoCurrencyDetailView(RetrieveAPIView):
#     queryset = CryptoCurrency.objects.all()
#     serializer_class = CryptoCurrencySerializer
#     permission_classes = (permissions.AllowAny, )

# class CryptoCurrencyCreateView(CreateAPIView):
#     queryset = CryptoCurrency.objects.all()
#     serializer_class = CryptoCurrencySerializer
#     permission_classes = (permissions.AllowAny, )    # in doubt: if complicate the use?

# class CryptoCurrencyUpdateView(UpdateAPIView):
#     queryset = CryptoCurrency.objects.all()
#     serializer_class = CryptoCurrencySerializer
#     permission_classes = (permissions.AllowAny, )    # in doubt: if complicate the use?

# class CryptoCurrencyDeleteView(DestroyAPIView):
#     queryset = CryptoCurrency.objects.all()
#     serializer_class = CryptoCurrencySerializer
#     permission_classes = (permissions.AllowAny, )    # in doubt: if complicate the use?

# class MetricListView(ListAPIView):
#     queryset = Metric.objects.all()
#     serializer_class = MetricSerializer
#     permission_classes = (permissions.AllowAny, )

# class MetricDetailView(ListAPIView):
#     serializer_class = MetricSerializer
#     permission_classes = (permissions.AllowAny, )

#     def get_queryset(self):
        
#         name = self.kwargs['name']
#         # name = self.request.query_params.get('name', None)
#         print('\n\nname = ', name, '\n\n')

#         with connection.cursor() as cursor:
#             cursor.execute('''SELECT * FROM maker_cryptocurrency c, maker_metric m 
#                 WHERE c.id = m.crypto_currency_id AND c.name LIKE '%%%s%%' AND m.timeslot_id = (
#                 SELECT MAX(timeslot_id) FROM maker_metric WHERE crypto_currency_id = c.id 
#             )''' % name)
#             queryset = cursor.fetchall()
#         return queryset


# def test_view(request):
#     return HttpResponse("Test view: passed.")

from rest_framework import viewsets
from maker.models import *
from .serializers import CryptoCurrencySerializer, RelatedNewsSerializer

class CryptoCurrencyViewSet(viewsets.ModelViewSet):
    serializer_class = CryptoCurrencySerializer
    queryset = CryptoCurrency.objects.all()

class RelatedNewsViewSet(viewsets.ModelViewSet):
    serializer_class = RelatedNewsSerializer
    queryset = RelatedNews.objects.all()

    