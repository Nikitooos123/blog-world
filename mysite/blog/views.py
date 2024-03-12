from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import logging
from . import services

logger = logging.getLogger(__name__)

''' Представление редактирования поста '''
@login_required
def post_edit(request, id):
    post = services.post_query_database(post_id=id, user_id=request.user.id)
    form = services.form_edit_post(request, post)
    if request.method == 'POST':
        return redirect(request.POST['return_to'])
    data = {'form': form}
    return render(request, 'blog/post_edit.html', data)

''' Представление удаления поста '''
@login_required
def post_delete(request, id):
    post = services.post_query_database(post_id=id, user_id=request.user.id)
    post.delete()
    services.cache_posts_database(request.user.id)
    return redirect(request.META.get('HTTP_REFERER'))


''' Представление лайков поста '''

def like(request):
    data = services.likes_processing(id=(request.POST.get('id')), user=request.user)
    return JsonResponse(data)


''' Детальное представление поста '''

@login_required
def post_detail(request, user, id):
    post = services.post_query_database(user_id=user, post_id=id)
    form = services.save_coment_post(request, post)
    if request.method == 'POST':
            return redirect(f'/post:{id}')
    data = {'post': post, 'form': form, 'comment': services.list_coments_post(post_id=id)}
    return render(request, 'blog/post_detail.html', data)


''' Представление профиля пользователя '''

@login_required
def profiles(request, id):
    users, profiles = services.enquiry_user_profile(user_id=id)
    posts = services.enquiry_posts_list(user_id=id)
    form = services.save_post(request)
    if request.method == 'POST':
        return redirect(f'/user={id}')
    return render(request, 'blog/profiles.html', {'user': users, 'profiles': profiles, 'form': form, 'posts': posts})

