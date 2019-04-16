from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.UserListView.as_view()),
    path('advice/<int:num>+<type>', views.currency_advice, name="advice"),
]