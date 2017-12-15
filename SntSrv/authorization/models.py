from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_names =  models.CharField(
        blank=True,
        max_length=128,
        null=True,
        verbose_name='Отчество',
    )
    phone =  models.CharField(
        blank=True,
        max_length=128,
        null=True,
        verbose_name='Телефон',
    )
    '''
    address =  models.CharField(
        blank=True,
        max_length=128,
        null=True,
        verbose_name='Адрес доставки',
    )
    '''
    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
