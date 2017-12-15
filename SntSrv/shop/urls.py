from django.conf.urls import url
from django.contrib import admin
from .views import (
    get_category_list,
    get_product,
    get_shopping_cart,
    #get_xls_parse,
)

urlpatterns = [
    url(
        r'^каталог$',
        get_category_list,
        name='category_list',
    ),
    url(
        r'^каталог/страница_(?P<page_number>[0-9]+)$',
        get_category_list,
        name='category_list_paginator_page',
    ),
    url(
        r'^категория_(?P<category_id>[0-9]+)$',
        get_category_list,
        name='category_page',
    ),
    url(
        r'^категория_(?P<category_id>[0-9]+)/страница_(?P<page_number>[0-9]+)$',
        get_category_list,
        name='category_page_paginator_page',
    ),
    url(
        r'^товар_(?P<product_id>[0-9]+)$',
        get_product,
        name='product',
    ),
    url(
        r'^корзина$',
        get_shopping_cart,
        name='shopping_cart',
    ),
    #url(r'^xls$', get_xls_parse,),
]
