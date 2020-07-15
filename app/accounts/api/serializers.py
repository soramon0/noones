from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        min_length=8,
        style={'input_style': 'password'},
        trim_whitespace=False
    )


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=8,
        style={'input_style': 'password'},
        trim_whitespace=False
    )
    new_password = serializers.CharField(
        min_length=8,
        style={'input_style': 'password'},
        trim_whitespace=False
    )
    confirm_password = serializers.CharField(
        min_length=8,
        style={'input_style': 'password'},
        trim_whitespace=False
    )

    def validate_new_password(self, value):
        validate_password(value)
        return value
