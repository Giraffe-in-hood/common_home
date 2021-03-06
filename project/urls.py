"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from drf_auto.views import DRFDocsView

from advert.views import (
    AdvertCrudView, AdvertListView, CategoryListView, AdvertRetrieveUpdateDeleteView,
    ImageAdUploadView, ImageAdDeleteView
)
from users.views import LoginView, LogoutView, RegistrationView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-docs/$', DRFDocsView.as_view(), name='docs'),
    url(r'^category/list/$', CategoryListView.as_view()),
]


# advert
urlpatterns += [
    url(r'^advert/$', AdvertCrudView.as_view()),
    url(r'^advert/(?P<pk>\d+)/$', AdvertRetrieveUpdateDeleteView.as_view()),
    url(r'^advert/list/$', AdvertListView.as_view()),
    url(r'^advert/images/(?P<advert>\d+)/$', ImageAdUploadView.as_view()),
    url(r'^advert/images/(?P<advert>\d+)/delete/(?P<pk>\d+)/$', ImageAdDeleteView.as_view())
]


# register
urlpatterns += [
    url(r'auth/login/$', LoginView.as_view()),
    url(r'auth/logout/$', LogoutView.as_view()),
    url(r'auth/register/$', RegistrationView.as_view()),
]
