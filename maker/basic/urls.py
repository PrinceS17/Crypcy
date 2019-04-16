from django.urls import path, re_path
from . import views
# from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('by_vol/', views.sort_by_vol, name='sort by vol'),
    path('by_pri/', views.sort_by_pri, name='sort by pri'),
    path('by_sup/', views.sort_by_sup, name='sort_by_sup'),
    path('by_util/', views.sort_by_util, name='sort_by_util'),
    path('pref/<pref>/', views.search_by_pref, name= 'search_by_pref')
]