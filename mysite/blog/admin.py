from django.contrib import admin
from .models import UserPost, CommentPost


@admin.register(UserPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'image', 'created']
    list_filter = ['created']

@admin.register(CommentPost)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'user', 'body', 'created', 'active']
    list_filter = ['created']