"""
Сериалайзеры для пользователей

"""
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User


class UserMinSerializer(serializers.ModelSerializer):
    """
    Минимальный сериалайзер для пользователя.

    """
    class Meta:
        model = User
        fields = 'username', 'first_name', 'last_name', 'image', 'email'


class LoginRequestSerializer(serializers.Serializer):
    """
    Сериалайзер для входа.

    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class RegistrationSerializer(serializers.Serializer):
    """
    Сериалайзер для регистрации.

    """
    email = serializers.EmailField(required=True)
    name = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    check_password = serializers.CharField(required=True)

    def validate(self, attrs):
        passwd, passwd_2 = attrs.get('password'), attrs.get('check_password')
        if passwd != passwd_2:
            raise ValidationError({'password': 'Пароли должны быть равны'})

        email = attrs.get('email', None)
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'Пользователь с таким email уже зарегистрирован'})
