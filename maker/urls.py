from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:price1>-<int:price2>/adv1/', views.adv1, name='adv1'),
    path('<int:price>/adv2/', views.adv2, name='adv2'),
]