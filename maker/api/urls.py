from django.urls import path
from . import views
from .views import (
    CryptoCurrencyListView,
    CryptoCurrencyDetailView,
    CryptoCurrencyCreateView,
    CryptoCurrencyUpdateView,
    CryptoCurrencyDeleteView,
    MetricListView,
    test_view
)

urlpatterns = [
    path('', CryptoCurrencyListView.as_view(), name='index'),
    path('create/', CryptoCurrencyCreateView.as_view(), name='create'),
    path('<pk>/', CryptoCurrencyDetailView.as_view(), name='detail'),
    path('<pk>/update/', CryptoCurrencyUpdateView.as_view(), name='update'),
    path('<pk>/delete/', CryptoCurrencyDeleteView.as_view(), name='delete'),
    # path('metric/', MetricListView.as_view(), name='metric'),
    # path('metric/', views.test_view, name='metric'),      # not work
]
