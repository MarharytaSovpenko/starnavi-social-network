from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer as BaseTokenObtainSerializer,
)
from django.utils.timezone import now


class TokenObtainPairSerializer(BaseTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        token = BaseTokenObtainSerializer.get_token(user)
        user.last_login = now()
        user.save()
        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "last_login", "last_request")
