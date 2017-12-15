from django.shortcuts import render
from shop.models import Category, Product
from django.core.serializers import serialize
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from django.core.mail import send_mail
import sys
from .models import Slider, Page
from .functions import get_base_menus
from django.http import Http404


def get_main_page(request):
    context = {}
    get_base_menus(context)
    context['category_list'] = Category.objects.filter(parent=None)
    context['slider'], has_slider = Slider.objects.get_or_create(pk=1, name='Главной страницы')
    context['page_name'] = 'Главная'
    return render(request, 'plugins/main_page.html', context)


def get_page(request, page_slug):
    context = {}
    try:
        context['page'] = Page.objects.get(url=page_slug)
        get_base_menus(context)
        context['category_list'] = Category.objects.filter(parent=None)
        if context['page'].slider:
            context['slider'] = context['page'].slider
        return render(request, 'plugins/page.html', context)
    except:
        raise Http404("Poll does not exist")
    


'''
@csrf_exempt
def send_email(request):
    if (
        request.POST
        and 'name' in request.POST
        and 'email' in request.POST
        and 'phone' in request.POST
        and 'mes' in request.POST
    ):
        subject='Заявка от %s' % (request.POST['name'])
        message='%s%s\n%s%s\n%s%s\n\n%s\n\n%s' % (
            'Отправитель: ',
            request.POST['name'],
            'E-mail: ',
            request.POST['email'],
            'Телефон: ',
            request.POST['phone'],
            'Текст письма: ',
            request.POST['mes'],
        )
        from_email='sntsrv@mail.ru'
        recipient_list=['santehservis72@mail.ru']
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list
        )
    return HttpResponse('try_send_email', content_type='text/html')
'''
