from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
from .services import post_query_database, save_coment_post, list_coments_post, likes_processing, \
    enquiry_posts_list, enquiry_user_profile, save_post, cache_posts_database, form_edit_post

logger = logging.getLogger(__name__)

''' Представление редактирования поста '''
@login_required
def post_edit(request, id):
    post = post_query_database(post_id=id, user_id=request.user.id)
    form = form_edit_post(request, post)
    if request.method == 'POST':
        return redirect(request.POST['return_to'])
    data = {'form': form}
    return render(request, 'blog/post_edit.html', data)

''' Представление удаления поста '''
@login_required
def post_delete(request, id):
    post = post_query_database(post_id=id, user_id=request.user.id)
    post.delete()
    cache_posts_database(request.user.id)
    return redirect(request.META.get('HTTP_REFERER'))


''' Представление лайков поста '''

def like(request):
    data = likes_processing(id=request.POST.get('id'), user=request.user)
    return JsonResponse(data)


''' Детальное представление поста '''

@login_required
def post_detail(request, user, id):
    post = post_query_database(user_id=user, post_id=id)
    form = save_coment_post(request, post)
    if request.method == 'POST':
            return redirect(f'/post:{id}')
    data = {'post': post, 'form': form, 'comment': list_coments_post(post_id=id)}
    return render(request, 'blog/post_detail.html', data)


''' Представление профиля пользователя '''

@login_required
def profiles(request, id):
    users, profiles = enquiry_user_profile(user_id=id)
    posts = enquiry_posts_list(user_id=id)
    form = save_post(request)
    if request.method == 'POST':
        return redirect(f'/user={id}')
    return render(request, 'blog/profiles.html', {'user': users, 'profiles': profiles, 'form': form, 'posts': posts})

