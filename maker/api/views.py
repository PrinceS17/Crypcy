from rest_framework import permissions
from django.http import HttpResponse
from django.db import connection
from maker.sql_operation import dictfetchall


from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    UpdateAPIView
)
from maker.models import CryptoCurrency, Metric

#Added by Zou
from maker.models import User, RelatedNews, Log, Timeslot

from .serializers import CryptoCurrencySerializer, MetricSerializer

#added by Zou
from .serializers import UserSerializer, RelatedNewsSerializer, LogSerializer,TimeslotSerializer

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

# class MetricDetailView(RetrieveAPIView):
#     with connection.cursor() as cursor:
#         cursor.execute()

#     serializer_class = MetricSerializer
#     permission_classes = (permissions.AllowAny, )

# Begin---Zou

#User's insert, update, delete
class UserListView(ListAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes= (permissions.AllowAny, )

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny, )

#RelatedNews insert, update, delete, display
class RelatedNewsListView(ListAPIView):
    queryset=RelatedNews.objects.all()
    serializer_class=RelatedNewsSerializer
    permission_classes= (permissions.AllowAny, )

class RelatedNewsDetailView(RetrieveAPIView):
    queryset = RelatedNews.objects.all()
    serializer_class = RelatedNewsSerializer
    permission_classes = (permissions.AllowAny, )

class RelatedNewsCreateView(CreateAPIView):
    queryset = RelatedNews.objects.all()
    serializer_class = RelatedNewsSerializer
    permission_classes = (permissions.AllowAny, )

class RelatedNewsUpdateView(UpdateAPIView):
    queryset = RelatedNews.objects.all()
    serializer_class = RelatedNewsSerializer
    permission_classes = (permissions.AllowAny, )

class RelatedNewsDeleteView(DestroyAPIView):
    queryset = RelatedNews.objects.all()
    serializer_class = RelatedNewsSerializer
    permission_classes = (permissions.AllowAny, )

#Log insert, update, delete, display
class LogListView(ListAPIView):
    queryset=Log.objects.all()
    serializer_class=LogSerializer
    permission_classes= (permissions.AllowAny, )

class LogDetailView(RetrieveAPIView):
    queryset=Log.objects.all()
    serializer_class=LogSerializer
    permission_classes= (permissions.AllowAny, )

class LogCreateView(CreateAPIView):
    queryset=Log.objects.all()
    serializer_class=LogSerializer
    permission_classes= (permissions.AllowAny, )

class LogUpdateView(UpdateAPIView):
    queryset=Log.objects.all()
    serializer_class=LogSerializer
    permission_classes= (permissions.AllowAny, )

class LogDeleteView(DestroyAPIView):
    queryset=Log.objects.all()
    serializer_class=LogSerializer
    permission_classes= (permissions.AllowAny, )


# timeslot insert, update, delete, display
class TimeslotListView(ListAPIView):
    queryset=Timeslot.objects.all()
    serializer_class=TimeslotSerializer
    permission_classes= (permissions.AllowAny, )

class TimeslotDetailView(RetrieveAPIView):
    queryset=Timeslot.objects.all()
    serializer_class=TimeslotSerializer
    permission_classes= (permissions.AllowAny, )

class TimeslotCreateView(CreateAPIView):
    queryset=Timeslot.objects.all()
    serializer_class=TimeslotSerializer
    permission_classes= (permissions.AllowAny, )

class TimeslotUpdateView(UpdateAPIView):
    queryset=Timeslot.objects.all()
    serializer_class=TimeslotSerializer
    permission_classes= (permissions.AllowAny, )

class TimeslotDeleteView(DestroyAPIView):
    queryset=Timeslot.objects.all()
    serializer_class=TimeslotSerializer
    permission_classes= (permissions.AllowAny, )

# End----Zou
def test_view(request):
    return HttpResponse("Test view: passed.")
