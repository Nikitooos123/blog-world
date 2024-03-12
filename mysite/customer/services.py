from django.shortcuts import get_object_or_404
from .models import Profile
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.core.cache import cache
from blog.models import UserPost


def user_subscribtion(user, id) -> dict:
    """ Добавляем/Удаляем пользователя из писка подписчиков """

    profile = get_object_or_404(Profile, user=id)
    if user in profile.subscribers.all():
        profile.subscribers.remove(user)
    else:
        profile.subscribers.add(user)
    profile.save()
    return {'sub': profile.subscribers.count()}


def edit_profiles(request):
    """ Валидация формы изменения данных пользователя """

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return user_form, profile_form
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return user_form, profile_form


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



def user_registration_form(request):
    """ Валидация формы регистрации пользователя """

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return new_user
    else:
        user_form = UserRegistrationForm()
        return user_form