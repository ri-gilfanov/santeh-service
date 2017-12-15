from django import forms
from .models import Brand, Product

class ProductFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        strip=True,
    )
    brand = forms.ModelChoiceField(
        empty_label='все бренды',
        label='бренд',
        required=False,
        queryset=None,
    )
    price_min = forms.DecimalField(
        decimal_places=2,
        label='мин. цена',
        max_value=999999,
        min_value=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            'step': 0.01,
        }),
    )
    price_max = forms.DecimalField(
        decimal_places=2,
        label='макс. цена',
        max_value=999999,
        min_value=0,
        max_digits=10,
        required=False,
        widget=forms.NumberInput(attrs={
            'step': 0.01,
        }),
    )
    def __init__(self, product_category_list=None, *args, **kwargs):
        super(ProductFilterForm, self).__init__(*args, **kwargs)
        if product_category_list:
            product_list=Product.objects.filter(categories__id__in=product_category_list)
            brand_list = Brand.objects.filter(products__in=product_list)
            self.fields['brand'].queryset = brand_list.distinct()
            self.fields['search_query'].label = "Поиск в категории"
        else:
            self.fields['brand'].queryset = Brand.objects.all()
            self.fields['search_query'].label = "Поиск в каталоге"
