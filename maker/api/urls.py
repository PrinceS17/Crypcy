from django.urls import path
from . import views
from .views import (
    CryptoCurrencyListView,
    CryptoCurrencyDetailView,
    CryptoCurrencyCreateView,
    CryptoCurrencyUpdateView,
    CryptoCurrencyDeleteView,
    MetricListView,
    test_view,

    # Begin---Added by Zou
    UserListView,
    UserCreateView,
    UserDetailView,
    UserUpdateView,
    UserDeleteView,

    LogListView,
    LogCreateView,
    LogDetailView,
    LogUpdateView,
    LogDeleteView,

    RelatedNewsListView,
    RelatedNewsCreateView,
    RelatedNewsDetailView,
    RelatedNewsUpdateView,
    RelatedNewsDeleteView,

    TimeslotListView,
    TimeslotCreateView,
    TimeslotDetailView,
    TimeslotUpdateView,
    TimeslotDeleteView

    #End---Zou
)

urlpatterns = [
    path('', CryptoCurrencyListView.as_view(), name='index'),
    path('create/', CryptoCurrencyCreateView.as_view(), name='create'),
    path('metric/', MetricListView.as_view(), name='metric'),
    path('Timeslot/', TimeslotListView.as_view(), name='Timeslot'),
    
    # path('metric/', views.test_view, name='metric'),      # not work
    path('<pk>/', CryptoCurrencyDetailView.as_view(), name='detail'),
    path('<pk>/update/', CryptoCurrencyUpdateView.as_view(), name='update'),
    path('<pk>/delete/', CryptoCurrencyDeleteView.as_view(), name='delete'),

    #Begin ---Zou

    # User database insert, update, delete, display
    path('', UserListView.as_view(), name='index'),
    path('<pk>/', UserDetailView.as_view(), name='User_detail'),
    path('User_create/', UserCreateView.as_view(), name='User_create'),
    path('<pk>/update/', UserUpdateView.as_view(), name='update'),
    path('<pk>/delete/', UserDeleteView.as_view(), name='delete'),

    # Log database insert, update, delete, display
    path('Log/', LogListView.as_view(), name='index'),
    path('<pk>/', LogDetailView.as_view(), name='Log_detail'),
    path('Log_Create/', LogCreateView.as_view(), name='Log_Create'),
    path('<pk>/update/', LogUpdateView.as_view(), name='update'),
    path('<pk>/delete/', LogDeleteView.as_view(), name='delete'),

    # RelatedNews database insert, update, delete, display
    path('', RelatedNewsListView.as_view(), name='index'),
    path('RelatedNews_Create/', RelatedNewsCreateView.as_view(), name='RelatedNews_Create'),
    path('<pk>/', RelatedNewsDetailView.as_view(), name='RelatedNews_detail'),
    path('<pk>/update/', RelatedNewsUpdateView.as_view(), name='update'),
    path('<pk>/delete/', RelatedNewsDeleteView.as_view(), name='delete'),

    # Timeslot inssert, update, delete, display
    #path('Timeslot_Create/', TimeslotCreateView.as_view(), name='Timeslot_Create'),
    #path('<pk>/', TimeslotDetailView.as_view(), name='Timeslot_detail'),
    #path('<pk>/update/', TimeslotUpdateView.as_view(), name='update'),
    #path('<pk>/delete/', TimeslotDeleteView.as_view(), name='delete'),
    #path('')
    #End----Zou
]
