from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Advert, Category, ImageAd
from .serializers import AdvertSer, AdRequestGetSer, CategorySer, CategoryRecSer
from rest_framework.generics import ListAPIView


class AdvertCrudView(APIView):
    """
    Тут мы пишем супер ЯЕстьГрут
    Который смотрит объект, меняет, добавляет и удаляет
    С помощью запросиков
    """
    def get(self, request, *args, **kwargs):
        # Получаем данные от пользователя. Если данные плохие, возврвщаем ошибку 400.
        reqser = AdRequestGetSer(data=request.query_params)
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
        ser = AdvertSer(instance=obj)
        return Response(data=ser.data)

    def post(self, request, *args, **kwargs):
        pass

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







