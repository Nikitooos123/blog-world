from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import PostForm, CommentForm
from .models import UserPost, CommentPost
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from customer.models import Profile


''' Представление комментариев '''

@require_POST
def comments(request, post_id):
    post = get_object_or_404(PostForm, id=post_id)
    comment = None
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
    return render(request, 'blog/comment_post.html', {'post': post, 'form': form, 'comment': comment})


''' обработчик лайков поста '''

def like(request):
    post = get_object_or_404(UserPost, pk=request.POST.get('id'))
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    post.save()
    data = {'likes_count': post.likes.count()}
    return JsonResponse(data)


''' Детальное представление поста '''

@login_required
def post_detail(request, id):
    post = get_object_or_404(UserPost, id=id)
    comment = CommentPost.objects.filter(post=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            comment_form = form.save(commit=False)
            comment_form.post = post
            comment_form.user = request.user
            comment_form.save()
    else:
        form = CommentForm(request.GET)
    return render(request, 'blog/post_detail.html', {'post': post, 'form': form, 'comment': comment})


''' Представление профиля пользователя '''

@login_required
def profiles(request, id):
    users = User.objects.filter(id=id)[0]
    profiles = get_object_or_404(Profile, user=id)
    posts = UserPost.objects.filter(user=id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form_post = form.save(commit=False)
            form_post.user = request.user
            form_post.save()
            return redirect('profiles')
    else:
        form = PostForm(request.GET)
    return render(request, 'blog/profiles.html', {'user': users, 'profiles': profiles, 'form': form, 'posts': posts})


''' Представление поста '''

def post_complete(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form_post = form.save(commit=False)
            form_post.user = request.user
            form_post.save()
            return redirect('profiles')
    else:
        form = PostForm(request.GET)
    return render(request, 'blog/post_complete.html', {'form': form})