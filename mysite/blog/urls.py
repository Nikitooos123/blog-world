from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post_complete/', views.post_complete, name='post_complete'),
    path('user=<int:id>/', views.profiles, name='profiles'),
    path('post:<str:id>/', views.post_detail, name='post_detail'),
    path('like/', views.like, name='likes'),
]