from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.registration.views import RegisterView
from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('username', 'email', 'name', 'gender', 'interest_tag', )

class CustomRegistrationSerializer(RegisterSerializer):
    name = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    interest_tag = serializers.CharField(required=False)

    def custom_signup(self, request, user):
        user.name = self.validated_data.get('name', '')
        user.gender = self.validated_data.get('gender', '')
        user.interest_tag = self.validated_data.get('interest_tag', '')
        user.save(update_fields=['name', 'gender', 'interest_tag'])

# for test
class CustomRegistrationView(RegisterView):
    serializer_class = CustomRegistrationSerializer