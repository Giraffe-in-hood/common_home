from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Advert, Category, ImageAd
from .serializers import (
    AdvertSer, AdRequestGetSer, CategorySer,
    CategoryRecSer, AdvertCreateSerializer
)


class AdvertCrudView(APIView):
    """
    Тут мы пишем супер ЯЕстьГрут.
    Который смотрит объект, меняет, добавляет и удаляет.
    С помощью запросиков.

    """
    serializer_classes = {
        'get': {
            'in': AdRequestGetSer,
            'out': AdvertSer
        },
        'post': {
            'in': AdvertCreateSerializer,
            'out': AdvertSer
        }
    }

    def get_serializer_class(self, for_req=False):
        """
        Возвращает сериалайзер для обработки данных.

        :param bool for_req: Флаг, указвающий для чего сериалайзер.

        :return: Сериалайзер для обработки запроса.
        :rtype: type(rest_framework.serializers.Serializer)

        """
        return self.serializer_classes.get(
            self.request.method.lower(), {}).get('in' if for_req else 'out')

    def dispatch(self, request, *args, **kwargs):
        """
        Проверяем авторизацию для метода.

        """
        if request.method.lower() == 'get':
            return super().dispatch(request, *args, **kwargs)
        if request.user and request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        return Response(status=401)

    def get(self, request, *args, **kwargs):
        """
        Просмотреть конкретное объявление.

        """
        # Получаем данные от пользователя. Если данные плохие, возврвщаем ошибку 400.
        reqser = self.get_serializer_class(True)(data=request.query_params)
        if reqser.is_valid() is True:
            pk = reqser.validated_data["pk"]
        else:
            return Response(status=400, data=reqser.errors)

        # Достаем данные из БД, если данных нет, то возвращаем 404
        try:
            obj = Advert.objects.get(pk=pk)
        except Advert.DoesNotExist:
            return Response(status=404)

        # Стерилизуем объект из БД, и возвращаем пользователюю
        ser = self.get_serializer_class()(instance=obj)
        return Response(data=ser.data)

    def post(self, request, *args, **kwargs):
        """
        Создание объявлния.

        """
        data = request.data.copy()
        data['author'] = request.user

        reqser = self.get_serializer_class(True)(data=request.data)
        reqser.is_valid(raise_exception=True)

        reqser.save()

        return Response(data=self.get_serializer_class()(reqser.instance).data, status=201)

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass


class AdvertListView(ListAPIView):
    """
    Список объявлений
    """
    serializer_class = AdvertSer
    queryset = Advert.objects.all()

    def get_queryset(self):
        # Кладем в сериалайзер данные пользователя
        ser = CategoryRecSer(data=self.request.query_params)
        if ser.is_valid() is True:  # Проверяем что пользователь отприавл правильные данные для фильтрации
            queryset = self.queryset  # Копируем всю табличку в переменную
            # Если отправил категории, то фильтруем по категориям
            cts = ser.validated_data.get("cts", [])
            if cts:
                queryset = queryset.filter(categories__pk__in=cts)
            # Если отправил поисковый запрос то ищем в имени
            query = ser.validated_data.get("query", "")
            if query:
                queryset = queryset.filter(name__icontains=query)
            # Если отправил тип, то фильтруем по типу
            types = ser.validated_data.get("types", None)
            if types is not None:
                queryset = queryset.filter(types=types)
            # В конце возвращаем табличку исключая дулбликаты
            return queryset.distinct()
        # Если данные пользователя неверные, возвращаем всю табличку
        return self.queryset.all()


class CategoryListView(ListAPIView):
    """
    Список категорий
    """
    serializer_class = CategorySer
    queryset = Category.objects.all()







