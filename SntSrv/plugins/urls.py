from django.conf.urls import url
from django.contrib import admin
from .views import (
    get_main_page,
    get_page,
    #send_email,
)

urlpatterns = [
    url(r'^$', get_main_page, name='main_page'),
    url(r'^(?P<page_slug>\w+)$', get_page, name='page'),
]
