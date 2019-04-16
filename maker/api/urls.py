# from django.urls import path, re_path
# from . import views
# from .views import (
#     CryptoCurrencyListView,
#     CryptoCurrencyDetailView,
#     CryptoCurrencyCreateView,
#     CryptoCurrencyUpdateView,
#     CryptoCurrencyDeleteView,
#     MetricListView,
#     MetricDetailView,
#     test_view
# )

# urlpatterns = [
#     path('', CryptoCurrencyListView.as_view(), name='index'),
#     path('create/', CryptoCurrencyCreateView.as_view(), name='create'),
#     path('metric/', MetricListView.as_view(), name='metric'),
#     path('<pk>/', CryptoCurrencyDetailView.as_view(), name='detail'),
#     path('<pk>/update/', CryptoCurrencyUpdateView.as_view(), name='update'),
#     path('<pk>/delete/', CryptoCurrencyDeleteView.as_view(), name='delete'),
#     # path('<pk>/metric/', MetricDetailView.as_view(), name='metric-detail'),     # not work
# ]

from maker.api.views import CryptoCurrencyViewSet, RelatedNewsViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'currency', CryptoCurrencyViewSet, base_name='currency')
router.register(r'news', RelatedNewsViewSet, base_name='news')
urlpatterns = router.urls

