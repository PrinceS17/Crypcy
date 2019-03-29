from django.urls import path

from .views import (
    CryptoCurrencyListView,
    CryptoCurrencyDetailView,
    CryptoCurrencyCreateView,
    CryptoCurrencyUpdateView,
    CryptoCurrencyDeleteView
)

urlpatterns = [
    path('', CryptoCurrencyListView.as_view(), name='index'),
    path('create/', CryptoCurrencyCreateView.as_view(), name='create'),
    path('<pk>', CryptoCurrencyDetailView.as_view(), name='detail'),
    path('<pk>/update/', CryptoCurrencyUpdateView.as_view(), name='update'),
    path('<pk>/delete/', CryptoCurrencyDeleteView.as_view(), name='delete')
]
