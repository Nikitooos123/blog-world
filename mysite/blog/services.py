from django.shortcuts import get_object_or_404
from .models import UserPost, CommentPost
from .forms import PostForm, CommentForm
from customer.models import Profile
from django.contrib.auth.models import User
from django.core.cache import cache


def enquiry_posts_list(user_id: int) -> UserPost:
    """ Получаем список постов по id пользователя """

    posts = cache.get(f'posts{user_id}')
    if not posts:
        cache_posts_database(user_id)
        posts = cache.get(f'posts{user_id}')
    return posts


def enquiry_user_profile(user_id: int) -> [User, Profile]:
    """ Получаем данные пользователя по id пользователя из базовой модели User и из дополнительной модели Profiles """

    users = cache.get(f'users{user_id}')
    profiles = cache.get(f'profiles{user_id}')
    if not users or profiles:
        cache_user_profile(user_id)
        users = cache.get(f'users{user_id}')
        profiles = cache.get(f'profiles{user_id}')
    return users, profiles


def list_coments_post(post_id: int) -> CommentPost:
    """ Получение списка комментариев к посту """

    comment = cache.get(f'comment{post_id}')
    if not comment:
        cache_coments_post(post_id)
        comment = cache.get(f'comment{post_id}')
    return comment


def cache_coments_post(post_id: int) -> None:
    """ Кэшируем коментарии постов из модели CommentPost по id Поста """

    cache.set(f'comment{post_id}', CommentPost.objects.filter(post=post_id), 100)


def cache_user_profile(user_id: int)  -> None:
    """ Кэшируем коментарии постов из модели CommentPost по id Поста """

    cache.set(f'users{user_id}', User.objects.filter(id=user_id)[0], 100)
    cache.set(f'profiles{user_id}', get_object_or_404(Profile, user=user_id), 100)


def cache_posts_database(user_id: int) -> None:
    """ Кэшируем список постов пользователя по id пользователя """

    cache.set(f'posts{user_id}', UserPost.objects.filter(user=user_id), 100)


def post_query_database(user_id: int, post_id: int) -> UserPost:
    """ Отправление запроса в базу данных для получения поста """

    post = enquiry_posts_list(user_id).get(id=post_id)
    return post


def save_post(request) -> [PostForm, None]:
    """ Обработка формы отправки поста """

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            form_post = form.save(commit=False)
            form_post.user = request.user
            form_post.save()
            cache_posts_database(request.user.id)
            return None
    else:
        form = PostForm(request.GET)
    return form


def save_coment_post(request, post: UserPost) -> [CommentForm, None]:
    """ Обработка формы отправки комментариев """

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment_form = form.save(commit=False)
            comment_form.post = post
            comment_form.user = request.user
            comment_form.save()
            cache_coments_post(post.id)
            return None
    else:
        form = CommentForm(request.GET)
    return form

def form_edit_post(request, post: UserPost) -> [PostForm, None]:
    """ Обработка формы редактирования поста """

    if request.method == 'POST':
        form = PostForm(data=request.POST, files=request.FILES, instance=post)
        if form.is_valid():
            form.save()
            cache_posts_database(request.user.id)
            return None
    else:
        form = PostForm(instance=post)
        return form

def likes_processing(id: int, user: UserPost) -> dict:
    """ Обработка нажатия на кнопку лайка """
    post = post_query_database(user.id, id)
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    post.save()
    return {'likes_count': post.likes.count(), 'liked': liked}