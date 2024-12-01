from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from rest_framework.authtoken.models import Token


class User(AbstractUser):

    USER_TYPE_CHOICES = (
        (1, 'campus-admin'),
        (2, 'campus-user'),
        (3, 'bookway-admin'),
        (4, 'bookway-user'),
        (5, 'admin'),
        (6, 'webapp'),
    )

    user_type = models.PositiveSmallIntegerField(null=True, blank=True, choices=USER_TYPE_CHOICES)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})


    objects = UserManager()

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["username"]

    def __str__(self):
        return self.username

