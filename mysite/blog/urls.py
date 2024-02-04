from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('delete<str:id>', views.post_delete, name='delete'),
    path('edit<str:id>/', views.post_edit, name='post_edit'),
    path('user=<int:id>/', views.profiles, name='profiles'),
    path('post:<str:id>/', views.post_detail, name='post_detail'),
    path('like/', views.like, name='likes'),
]