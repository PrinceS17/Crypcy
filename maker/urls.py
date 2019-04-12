from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:price1>-<int:price2>/adv1/', views.adv1, name='adv1'),
    path('<int:price>/adv2/', views.adv2, name='adv2'),
    path('<pref>/search_by_pref/', views.search_by_pref, name= 'search_by_pref'),
    path('sort_by_vol/', views.sort_by_vol, name='sort by vol'),
    path('sort_by_pri/', views.sort_by_pri, name='sort by pri'),
    path('sort_by_sup/', views.sort_by_sup, name='sort_by_sup'),
    path('sort_by_util/', views.sort_by_util, name='sort_by_util')


]
