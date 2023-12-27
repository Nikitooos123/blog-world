from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    data_of_brith = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users',
                              blank=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions', blank=True)

    def __str__(self):
        return f'Profile {self.user.username}'