from django.urls import include, path, re_path

from . import views

urlpatterns = [
    # path('', views.UserListView.as_view()),
    re_path(r'^advice?.*/$', views.currency_advice, name="advice"),     # extract username, num, type
]