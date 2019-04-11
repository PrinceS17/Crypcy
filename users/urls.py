from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('<int:num>+<int:type>/advice/', views.currency_advice, name="advice"),
]