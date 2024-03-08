from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
import logging
from django.core.cache import cache
from blog.models import UserPost

logger = logging.getLogger(__name__)

''' Обработчик подписки на пользователя '''
@login_required
def subscription(request):
    profile = get_object_or_404(Profile, user=request.POST.get('id'))
    if request.user in profile.subscribers.all():
        profile.subscribers.remove(request.user)
    else:
        profile.subscribers.add(request.user)
    profile.save()
    data = {'sub': profile.subscribers.count()}
    logger.info(('Подписка', data))
    return JsonResponse(data)


''' Представление страницы редактирования профиля '''

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    logger.info(('Редактирование', user_form, profile_form))
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})

''' Представление новостной страницы '''

@login_required
def news(request):
    posts = donwloads_posts_in_cache(request.user)
    return render(request, 'account/news.html', {'section': 'news', 'post_all': posts})



def donwloads_posts_in_cache(user) -> UserPost:
    """ Загрузка списка постов из кэша """

    posts = cache.get(f'news{user}')
    if not posts:
        donwloads_database_posts_in_cache(user)
        posts = cache.get(f'news{user}')
    return posts
def donwloads_database_posts_in_cache(user):
    """ Загрузка постов из базы данных и сортировка по подписки пользователя на автора  """
    """ С последующим сохранением списка в кэш """

    posts = list(UserPost.objects.all())
    subscrib = user.subscriptions.all()
    for post in posts:
        if post.user.profile in subscrib:
            posts.remove(post)
            posts.insert(0, post)
    cache.set(f'news{user}', posts, 100)


''' Представление формы регистрации '''

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    logger.info(('Регистрация', user_form))
    return render(request, 'account/register.html', {'user_form': user_form})

