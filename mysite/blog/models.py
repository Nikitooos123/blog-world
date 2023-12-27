from django.db import models
from django.conf import settings
from django.utils.text import slugify



''' Модель поста '''

class UserPost(models.Model):
    title = models.CharField(max_length=250)
    slug = slugify(title)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post/%Y/%m/%d/', blank=True, null=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_post', blank=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return self.title


''' Модель комментариев '''

class CommentPost(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='post_comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_comments')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]

    def __str__(self):
        return f'{self.post}{self.user}'