from django.db import models
from ckeditor.fields import RichTextField
from django.db.models.signals import post_delete
from django.dispatch import receiver
from djorm_pgfulltext.models import SearchManager
from djorm_pgfulltext.fields import VectorField
from SntSrv.functions import delete_image_at_object_delete, delete_image_at_object_change


class Category(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='название категории',
    )
    image = models.ImageField(
        blank=True,
        verbose_name='изображение',
        null=True,
        upload_to='categories/',
    )
    parent = models.ForeignKey(
        blank=True,
        related_name='children',
        null=True,
        to='self',
        verbose_name='родительская категория',
    )
    is_in_main_page = models.BooleanField(
        default=False,
        verbose_name='выводить на главной странице',
    )
    is_list_view = models.BooleanField(
        default=False,
        verbose_name='вывод товаров простым списком',
    )
    def save(self, *args, **kwargs):
        delete_image_at_object_change(post_object=self)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        if self.parent != None:
            return '%s (%s)' % (self.name, self.parent)
        else:
            return self.name

    class Meta:
        ordering = ['name', 'parent__name']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
post_delete.connect(receiver=delete_image_at_object_delete, sender=Category)


class Brand(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='бренд',
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'


class Product(models.Model):
    code = models.IntegerField(
        verbose_name='код товара',
        unique=True,
    )
    name = models.CharField(
        max_length=128,
        verbose_name='название товара',
        unique=True,
    )
    def get_product_image_path(instance, filename):
        return '%s/%s.%s' % (
            'products',
            instance.name,
            filename.split('.')[-1],
        )
    image = models.ImageField(
        blank=True,
        null=True,
        verbose_name='изображение',
        upload_to=get_product_image_path,
    )
    description = RichTextField(
        blank=True,
        config_name='product_config',
        null=True,
        verbose_name='описание товара',
    )
    characteristics = RichTextField(
        blank=True,
        config_name='product_config',
        null=True,
        verbose_name='характеристика товара',
    )
    categories = models.ManyToManyField(
        blank=True,
        related_name='products',
        to=Category,
        verbose_name='категории',
    )
    brand = models.ForeignKey(
        blank=True,
        null=True,
        related_name='products',
        to=Brand,
        verbose_name='бренд',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена',
    )
    last_edit_date = models.DateTimeField(
        auto_now=True,
        verbose_name='последнее изменение',
    )
    is_in_stock = models.BooleanField(
        default=True,
        verbose_name='есть в продаже'
    )
    search_index = VectorField()
    objects = SearchManager(
        #fields = ('name', 'description', 'characteristics',),
        config = 'pg_catalog.russian',
        search_field = 'search_index',
        auto_update_search_field = True
    )

    def save(self, *args, **kwargs):
        delete_image_at_object_change(post_object=self)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-price']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
post_delete.connect(receiver=delete_image_at_object_delete, sender=Product)


class Purchase(models.Model):
    last_name = models.CharField(
        max_length=128,
        verbose_name='фамилия',
    )
    first_name = models.CharField(
        max_length=128,
        verbose_name='имя',
    )
    middle_name = models.CharField(
        max_length=128,
        verbose_name='отчество',
    )
    address = models.CharField(
        max_length=128,
        verbose_name='адрес',
    )
    phone = models.CharField(
        max_length=128,
        verbose_name='телефон',
    )
    email = models.EmailField(
        blank=True,
        max_length=128,
        null=True,
        verbose_name='электронная почта',
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='сумма',
    )
    time = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата и время',
    )

    def __str__(self):
        return 'Заказ от %s' % (self.time.__str__())

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class PurchaseItem(models.Model):
    product = models.ForeignKey(
        to=Product,
        verbose_name='товар',
    )
    count = models.IntegerField(
        verbose_name='количество',
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='цена',
    )
    purchase = models.ForeignKey(
        to=Purchase,
        verbose_name='позиции в заказе',
    )

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
    
