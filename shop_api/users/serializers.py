from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

class BaseUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(required=True)

class AuthValidateSerializer(BaseUserSerializer):
    pass

class RegisterValidateSerializer(BaseUserSerializer):
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')

class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    code = serializers.CharField(min_length=6, max_length=6, required=True)

    