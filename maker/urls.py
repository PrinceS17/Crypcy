from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^get/(?P<name>.+)/$', views.get_currency, name='gets'),
    re_path(r'^search-coin/(?P<name>.+)/$', views.get_best_currency, name='interesting1'),
    re_path(r'^search-news/(?P<word>.+)/$', views.get_news, name='interesting2'),
    # path('advice/<int:num>+<type>/', views.currency_advice, name="advice"),
    path('basic/', include('maker.basic.urls')),

    path('<int:price1>-<int:price2>/adv1/', views.adv1, name='adv1'),
    path('<int:price>/adv2/', views.adv2, name='adv2'),
]