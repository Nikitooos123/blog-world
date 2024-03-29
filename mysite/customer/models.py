from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    data_of_brith = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users',
                              blank=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions', blank=True)

    def __str__(self):
        return f'Profile {self.user.username}'

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()