from rest_auth.registration.serializers import RegisterSerializer
# from rest_auth.registration.views import RegisterView
from rest_auth.serializers import UserDetailsSerializer
from rest_framework import permissions, serializers
from rest_framework.generics import RetrieveUpdateAPIView
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'name', 'gender', 'interest_tag', 'favorite')
        # fields = '__all__'

class CustomRegistrationSerializer(RegisterSerializer):
    name = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    interest_tag = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.gender = self.validated_data.get('gender', '')
        user.interest_tag = self.validated_data.get('interest_tag', '')
        user.save(update_fields=['name', 'gender', 'interest_tag'])
