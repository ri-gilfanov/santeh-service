from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from .models import Category, Brand, Product, PurchaseItem, Purchase
from django import forms
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

AdminSite.site_header = 'Панель управления сайтом ООО "Сантехсервис"'


class CategoryForm(forms.ModelForm):
    # Переопределение формы редактирования категории, добавлены ограничения на выбор родителя
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        parents = Category.objects.filter(parent=None)
        if 'instance' in kwargs and 'pk' in dir(kwargs['instance']):
            parents = parents.exclude(pk=kwargs['instance'].pk)
        self.fields['parent'].queryset = parents


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
    form = CategoryForm
    list_display = ['__str__', 'parent']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ['name',]


class ChangeProductsBrandForm(forms.Form):
    # Форма выбора бренда для выбранных товаров
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    brand = forms.ModelChoiceField(
        label='Бренд',
        queryset=Brand.objects.all(),
        required=False,
    )


def change_products_brand(modeladmin, request, queryset):
    # Изменить бренд выбранных товаров
    form = None
    if 'apply' in request.POST:
        form = ChangeProductsBrandForm(request.POST)
        if  form.is_valid():
            count = queryset.count()
            if request.POST['brand']:
                brand = Brand.objects.get(pk=request.POST['brand'])
            else:
                brand = None
            queryset.update(brand=brand)
            modeladmin.message_user(request, "Бренд %s применён к %i товарам." % (brand, count))
            return HttpResponseRedirect(request.get_full_path())
    context = {}
    context['opts']=modeladmin.model._meta
    selected_products = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
    if not form:
        context['form'] = ChangeProductsBrandForm(
            initial={
                '_selected_action': selected_products,
            },
        )
    context['product_list'] = queryset
    return TemplateResponse(request, 'admin/change_products_brand.html', context)
change_products_brand.short_description = "Изменить бренд выбранных товаров"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'price', 'is_in_stock', 'last_edit_date']
    search_fields = ['name', 'code', 'categories__name', 'brand__name']
    #raw_id_fields = ['brand', ]
    list_filter = ['categories', 'brand', 'is_in_stock']
    actions=[change_products_brand,]
    filter_horizontal = ['categories']



'''
class PurchaseItemsInline(admin.TabularInline):
    extra = 1
    model = PurchaseItem
    raw_id_fields = ['product']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    inlines = [
        PurchaseItemsInline,
    ]
    list_display = ['time', 'address']
'''
