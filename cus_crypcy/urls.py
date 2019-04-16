"""cus_crypcy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from users.views import CustomRegistrationView, CustomDetailView
from allauth.account.views import ConfirmEmailView

urlpatterns = [
    path('', include('rest_auth.urls')),
    path('admin/', admin.site.urls), 
    path('api-auth/', include('rest_framework.urls')),
    path('rest-auth/', include('rest_auth.urls')),
    re_path(r'^rest-auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),  # now in users/
    # path('rest-auth/registration/', CustomRegistrationView.as_view(), name="custom register"),    # alternative, but dirty
    path('users/', include('users.urls')),        # dirty solution to use advice (adv func 1)

    path('maker/', include('maker.urls')),
    path('api/', include('maker.api.urls')),
]
