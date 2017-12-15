from .models import Menu


def get_base_menus(context):
    '''Получить стандартные меню'''
    context['main_menu'], has_menu = Menu.objects.get_or_create(pk=1, name='Главное меню')
    context['sites_menu'], has_menu = Menu.objects.get_or_create(pk=2, name='Другие сайты компании')
