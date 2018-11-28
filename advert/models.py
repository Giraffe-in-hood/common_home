from django.contrib.auth import get_user_model
from django.db import models


# TODO: категории, адрес
class Category (models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Advert (models.Model):
    TYPES = (
        (0, "Продам"),
        (1, "Предложить помощь"),
        (2, "Нужна помощь"),
    )
    name = models.CharField(max_length=255)
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name='advert')
    types = models.IntegerField(choices=TYPES)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class ImageAd(models.Model):
    image = models.ImageField()
    advert = models.ForeignKey(Advert, related_name='ad_images')

