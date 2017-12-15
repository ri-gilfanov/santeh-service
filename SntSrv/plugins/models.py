from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from ckeditor.fields import RichTextField
from SntSrv.functions import delete_image_at_object_delete, delete_image_at_object_change


class Slider(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='название слайдера',
        unique=True,
    )
    grouping = models.SmallIntegerField(
        default=3,
        verbose_name='группировка по (число)',
    )

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'слайдер'
        verbose_name_plural = 'слайдеры'


class Slide(models.Model):
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='slides/',
    )
    text = models.CharField(
        blank=True,
        max_length=128,
        null=True,
        verbose_name='текст',
    )
    link = models.URLField(
        blank=True,
        null=True,
        verbose_name='ссылка',
    )
    position = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='позиция',
    )
    slider = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='slides',
        to=Slider,
        verbose_name='слайдер',
    )

    def save(self, *args, **kwargs):
        delete_image_at_object_change(post_object=self)
        super(Slide, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    class Meta:
        ordering = ['position', 'pk']
        verbose_name = 'слайд'
        verbose_name_plural = 'слайды'
post_delete.connect(receiver=delete_image_at_object_delete, sender=Slide)


'''РЕДАКТИРУЕМЫЕ СТРАНИЦЫ И ИЗОБРАЖЕНИЯ К НИМ'''
class Page(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='название страницы',
        unique=True,
    )
    url = models.SlugField(
        allow_unicode=True,
        verbose_name='ссылка',
        unique=True,
    )
    content = RichTextField(
        blank=True,
        config_name='page_config',
        null=True,
        verbose_name='содержание страницы',
    )
    slider = models.ForeignKey(
        blank=True,
        null=True,
        related_name='pages',
        to=Slider,
        verbose_name='слайдер',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'страница'
        verbose_name_plural = 'страницы'


class PageImage(models.Model):
    image = models.ImageField(
        verbose_name='изображение',
        upload_to='pages/',
    )
    page = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='page_images',
        to=Page,
        verbose_name='страница',
    )

    def save(self, *args, **kwargs):
        delete_image_at_object_change(post_object=self)
        super(PageImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'изображение страницы'
        verbose_name_plural = 'изображения страницы'
post_delete.connect(receiver=delete_image_at_object_delete, sender=PageImage)


'''МЕНЮ САЙТА'''
class Menu(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name='название меню',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'меню'
        verbose_name_plural = 'меню'


class MenuItem(models.Model):
    text = models.CharField(
        max_length=128,
        verbose_name='текст',
        unique=True,
    )
    url = models.CharField(
        max_length=128,
        verbose_name='ссылка',
    )
    position = models.SmallIntegerField(
        blank=True,
        null=True,
        verbose_name='позиция',
    )
    menu = models.ForeignKey(
        on_delete=models.CASCADE,
        related_name='menu_items',
        to=Menu,
        verbose_name='меню',
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['position', 'text']
        verbose_name = 'пункт меню'
        verbose_name_plural = 'пункты меню'
