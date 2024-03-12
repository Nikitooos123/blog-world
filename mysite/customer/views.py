from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
import logging

from . import services

logger = logging.getLogger(__name__)

''' Обработчик подписки на пользователя '''
@login_required
def subscription(request):
    data = services.user_subscribtion(user=request.user, id=request.POST.get('id'))
    logger.info(('Подписка', data))
    return JsonResponse(data)

''' Представление страницы редактирования профиля '''

@login_required
def edit(request):
    user_form, profile_form = services.edit_profiles(request=request)
    logger.info(('Редактирование', user_form, profile_form))
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


''' Представление новостной страницы '''

@login_required
def news(request):
    posts = services.donwloads_posts_in_cache(user=request.user)
    return render(request, 'account/news.html', {'section': 'news', 'post_all': posts})


''' Представление формы регистрации '''

def register(request):
    user = services.user_registration_form(request=request)
    if type(user) is User:
        return render(request, 'account/register_done.html', {'new_user': user})
    logger.info(('Регистрация', user))
    return render(request, 'account/register.html', {'user_form': user})

