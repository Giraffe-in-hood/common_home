from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Advert, Category, ImageAd
from django.contrib.auth import get_user_model


class AdRequestGetSer(serializers.Serializer):
    pk = serializers.IntegerField(min_value=0)


class AuthorSer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = 'id', 'email', 'first_name', 'last_name'


class ImageSer(serializers.ModelSerializer):
    class Meta:
        model = ImageAd
        fields = 'image',


class ImageCreateSer(serializers.ModelSerializer):
    class Meta:
        model = ImageAd
        fields = '__all__'


class AdvertSer(serializers.ModelSerializer):
    author = AuthorSer()
    images = ImageSer(many=True, source='ad_images')

    class Meta:
        model = Advert
        fields = '__all__'


class CategorySer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CategoryRecSer(serializers.Serializer):
    cts = serializers.ListField(child=serializers.IntegerField(min_value=0), required=False)
    query = serializers.CharField(required=False)
    types = serializers.ChoiceField(choices=Advert.TYPES, required=False)

    def validate(self, attrs):
        cts = attrs.get("cts", [])
        if cts and not Category.objects.filter(pk__in=cts).exists():
            raise ValidationError('ids is required field')
        return attrs


class AdvertCreateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для создания объявления.

    """
    class Meta:
        model = Advert
        fields = 'name', 'text', 'categories', 'types', 'author',


class AdvertUpdateSerializer(serializers.ModelSerializer):
    """
    Сериалайзер для изменения объявления.

    """
    class Meta:
        model = Advert
        fields = 'name', 'text', 'categories', 'types', 'status'
