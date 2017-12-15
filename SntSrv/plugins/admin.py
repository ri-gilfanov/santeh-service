from django.contrib import admin
from .models import Slide, Slider, Page, PageImage, Menu, MenuItem


class SlideInline(admin.TabularInline):
    model = Slide
    extra = 1


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    inlines = [
        SlideInline,
    ]

class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    inlines = [
        PageImageInline,
    ]


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [
        MenuItemInline,
    ]

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(MenuAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
