from django.contrib.auth import login, logout
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import LoginRequestSerializer, UserMinSerializer, RegistrationSerializer


class LoginView(APIView):
    """
    Вход.

    """
    serializer_in = LoginRequestSerializer
    serializer_out = UserMinSerializer

    def post(self, request, *args, **kwargs):
        # Валидируем данные.
        ser = self.serializer_in(data=request.data)
        ser.is_valid(raise_exception=True)
        email, passwd = ser.validated_data.get('email', None), ser.validated_data.get('password', None)

        # Проверяем верность данных в базе.
        user = User.objects.filter(email=email).first()
        if not user:
            return Response(data={'email': 'Не верный email'}, status=400)
        if not user.check_password(passwd):
            return Response(data={'password': 'Не верный пароль'}, status=400)

        # Авторизуем пользователя
        login(request, user)
        return Response(data=self.serializer_out(user).data, status=200)


class RegistrationView(APIView):
    """
    Регистрация.

    """
    serializer_in = RegistrationSerializer
    serializer_out = UserMinSerializer

    def post(self, request, *args, **kwargs):
        # Валидируем данные
        ser = self.serializer_in(request.data)
        ser.is_valid(raise_exception=True)

        # Достаем в переменные
        email = ser.validated_data.get('email', None)
        name = ser.validated_data.get('name', None)
        passwd = ser.validated_data.get('password', None)

        # создаем и авторизуем пользователя
        user = User.objects.create_user(email, passwd, first_name=name)
        login(request, user)

        # Отдаем ответ
        return Response(data=self.serializer_out(user).data, status=200)


class LogoutView(APIView):
    """
    Выход.

    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return Response()
