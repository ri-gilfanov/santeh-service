from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Category, Brand, Product
#import xlrd
from .forms import ProductFilterForm
from django.template.context_processors import csrf
from plugins.functions import get_base_menus
from .functions import move_in_shopping_cart


def get_category_list(request, page_number=1, category_id=None):
    context, filter_kw, form_kw = {}, {}, {}  # инициализация словарей
    get_base_menus(context)               # Получить стандартные меню
    context['category_list'] = Category.objects.filter(parent=None)
    context.update(csrf(request))             # генерация CSRF-токена
    if request.POST:                          # обработка POST-параметров
        move_in_shopping_cart(request)        # добавление и удаление товаров из корзины
    if request.GET:                           # обработка GET-параметров
        request.GET = request.GET.copy()      # заполнение словарей по GET-параметрам
        if 'brand' in request.GET and request.GET['brand']:
            filter_kw['brand'] = int(request.GET['brand'])
            form_kw['brand'] = int(request.GET['brand'])
        if 'price_min' in request.GET and request.GET['price_min']:
            filter_kw['price__gte'] = float(request.GET['price_min'])
            form_kw['price_min'] = float(request.GET['price_min'])
        if 'price_max' in request.GET and request.GET['price_max']:
            filter_kw['price__lte'] = float(request.GET['price_max'])
            form_kw['price_max'] = float(request.GET['price_max'])
        if 'search_query' in request.GET and request.GET['search_query']:
            form_kw['search_query'] = request.GET['search_query']
        context['GET_parameters'] = '?%s' % (request.GET.urlencode(request.GET))
    filter_kw['is_in_stock'] = True  # только товары, что есть на складе
    product_category_list = None     # инициализируем список категорий как None
    if category_id:  # если выбрана категория заполняем список категорий
        category = Category.objects.get(id=category_id)
        context['category_selected'] = category
        children = Category.objects.filter(parent__id=category_id)
        product_category_list = [child.id for child in children]
        product_category_list.append(category_id)
        filter_kw['categories__in'] = product_category_list
    # товары и пагинатор
    if 'search_query' in request.GET:
        product_list = Product.objects.search(request.GET['search_query'])
        product_list = product_list.filter(**filter_kw)
    else:
        product_list = Product.objects.filter(**filter_kw)
    if 'category_selected' in context and context['category_selected'].is_list_view:
        product_list = product_list.order_by('name')
        per_page = 50
    else:
        per_page = 12
    paginator = Paginator(object_list=product_list, per_page=per_page)
    page_number = int(page_number)
    full_slice = 13
    half_slice = full_slice // 2
    if page_number <= half_slice:
        context['paginator_start'] = 0
        context['paginator_end'] = full_slice + 1
    elif (
        page_number >= half_slice - 1
        and page_number <= paginator.num_pages - half_slice
    ):
        context['paginator_start'] = page_number - half_slice - 1
        context['paginator_end'] = page_number + half_slice + 1
    else:
        context['paginator_start'] = paginator.num_pages - full_slice
        context['paginator_end'] = paginator.num_pages + 1
    context['paginator_start_link'] = half_slice + 1
    context['paginator_end_link'] = paginator.num_pages - half_slice
    context['paginator_range'] = paginator.page_range
    context['paginator_page'] = paginator.page(number=page_number)
    for p in context['paginator_page']:
        if 'shopping_cart' in request.session and str(p.pk) in request.session['shopping_cart']:
            p.count = request.session['shopping_cart'][str(p.pk)]
    # форма фильтрации
    context['product_fiter_form'] = ProductFilterForm(
        product_category_list=product_category_list,
        initial=form_kw,
    )
    
    print(dir(context['product_fiter_form'].fields['search_query']))
    
    return render(request, 'shop/category_page.html', context)
        

def get_shopping_cart(request):
    context = {}
    get_base_menus(context)  # Получить стандартные меню
    context['category_list'] = Category.objects.filter(parent=None)
    if request.POST:
        move_in_shopping_cart(request)  # добавление и удаление товаров из корзины
    if 'shopping_cart' in request.session:
        context['product_list'] = Product.objects.filter(pk__in=request.session['shopping_cart'])
    else:
        context['product_list'] = []
    context['price_sum'] = 0
    for p in context['product_list']:
        p.count = request.session['shopping_cart'][str(p.pk)]
        context['price_sum'] += p.count * p.price
    return render(request, 'shop/shopping_cart.html', context)
        

def get_product(request, product_id):
    context = {}
    context['product'] = Product.objects.get(id=product_id)
    get_base_menus(context)         # Получить стандартные меню
    context['category_list'] = Category.objects.filter(parent=None)
    if request.POST:                    # Обработка POST-параметров
        move_in_shopping_cart(request)  # добавление и удаление товаров из корзины
    context['categories_selected'] = context['product'].categories
    return render(request, 'shop/product.html', context)



'''
from django.shortcuts import redirect
def get_xls_parse(request):
    book = xlrd.open_workbook('/home/radimir/Рабочий стол/прайс 08.11.16.xls',formatting_info=True)
    sheet = book.sheet_by_index(0)
    code_list = []
    for i in range(0, sheet.nrows):
        if type(sheet.row_values(i)[2]) is not str:
            code_list.append(int(sheet.row_values(i)[2]))
    product_list = Product.objects.filter(code__in=code_list)
    product_code_list = [p.code for p in product_list]
    code_list = [c for c in code_list if c not in product_code_list]
    print('не добавлены', code_list)
    for i in range(0, sheet.nrows):
        sheet.row_values(i)[0].replace('  ', ' ')
        sheet.row_values(i)[0].replace('  ', ' ')
        sheet.row_values(i)[0].replace('  ', ' ')
        sheet.row_values(i)[0].strip()
        if (
            type(sheet.row_values(i)[2]) is not str
            and int(sheet.row_values(i)[2]) in code_list
        ):
            try:
                Product.objects.update_or_create(
                    name=sheet.row_values(i)[0],
                    price=float(sheet.row_values(i)[1]),
                    code=sheet.row_values(i)[2],
                )
            except:
                print(sheet.row_values(i)[2], Product.objects.get(name=sheet.row_values(i)[0]).code, sheet.row_values(i)[0])
                product = Product.objects.get(name=sheet.row_values(i)[0])
                old_price = product.price
                product.price=float(sheet.row_values(i)[1])
                product.save()
                print(old_price, product.price)
    return redirect('/')


from django.shortcuts import redirect
def get_xls_parse(request):
    book = xlrd.open_workbook('/home/radimir/Рабочий стол/прайс 08.11.16.xls',formatting_info=True)
    sheet = book.sheet_by_index(0)
    for i in range(12, sheet.nrows):
        sheet.row_values(i)[0].replace('  ', ' ')
        sheet.row_values(i)[0].replace('  ', ' ')
        sheet.row_values(i)[0].replace('  ', ' ')
        sheet.row_values(i)[0].strip()
        row = [
            sheet.row_values(i)[0],
            sheet.row_values(i)[1],
            sheet.row_values(i)[2],
        ]
        if row[0] and row[1] and row[2]:
            print('test', row[2])
            products = Product.objects.filter(code=int(row[2])).update(price = float(row[1]))
    return redirect('/')
'''
