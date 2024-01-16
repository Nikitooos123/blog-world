from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('user=<int:id>/', views.profiles, name='profiles'),
    path('post:<str:id>/', views.post_detail, name='post_detail'),
    path('like/', views.like, name='likes'),
]