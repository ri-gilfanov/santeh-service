from django.shortcuts import render
from shop.models import Category, Product
from django.core.serializers import serialize
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from django.core.mail import send_mail
import sys
from plugins.models import Slider
from plugins.functions import get_base_menus


def view_404(request):
    context = {}
    get_base_menus(context)
    context['category_list'] = Category.objects.filter(parent=None)
    return render(request, '404.html', context, status=404)


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
