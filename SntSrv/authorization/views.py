from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.template.context_processors import csrf
from shop.models import Category
from plugins.functions import get_base_menus


def get_log_in(request):
    context = {}
    get_base_menus(context)
    context['category_list'] = Category.objects.filter(parent=None)
    context['page_name'] = 'Вход зарегистрированного пользователя'
    context.update(csrf(request))
    context['auth_form'] = AuthenticationForm()
    if (
        request.POST
        and 'username' in request.POST
        and 'password' in request.POST
        and 'csrfmiddlewaretoken' in request.POST
    ):
        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password'],
        )
        if user:
            auth.login(request, user)
            messages.success(
                request,
                '''
                <p>Успешная авторизация</p>
                ''',
            )
        else:
             messages.warning(
                request,
                '''
                <p>Ошибка авторизации</p>
                ''',
            )
    if not request.user.is_authenticated():
        return render(request, 'authorization/log_in.html', context)
    else:
        return redirect('/')


def get_log_out(request):
    auth.logout(request)
    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('/')
