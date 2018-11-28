from django.contrib import admin
from .models import Advert, Category, ImageAd


@admin.register(Advert)
class AdminAdvert(admin.ModelAdmin):
    filter_horizontal = "categories",



@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    pass


@admin.register(ImageAd)
class AdminImageAd(admin.ModelAdmin):
    pass
