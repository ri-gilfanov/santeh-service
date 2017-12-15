from django.conf.urls import url
from .views import get_log_in, get_log_out

urlpatterns = [
    url(r'^вход$', get_log_in, name='log_in'),
    url(r'^выход$', get_log_out, name='log_out'),
    url(r'^управление/login/$', get_log_in),
    url(r'^управление/logout/$', get_log_out),
]
