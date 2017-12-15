"""SntSrv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import include, url
from django.contrib import admin
from .views import (
    view_404,
    #send_email,
)
from django.conf.urls.static import static
from django.conf import settings

handler404 = 'SntSrv.views.view_404'

urlpatterns = [
    url(r'^', include('shop.urls')),
    url(r'^', include('authorization.urls')), # перед admin.site.urls
    url(r'^управление/', admin.site.urls),
    url(r'^', include('plugins.urls')),
    #url(r'^send_email$', send_email, name='send_email'),
]


urlpatterns.extend(
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
)


urlpatterns.extend(
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
)
from django.contrib import admin
