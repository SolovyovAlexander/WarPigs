from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    bricks = models.IntegerField(_('bricks'))
    rating = models.IntegerField(_('rating'))

    def __str__(self):
        return f'{self.email}'


class Raid(models.Model):
    user_to_raid = models.IntegerField(_('user to raid'))
    status = models.CharField(_('status'), max_length=24)
    preparation_time = models.TimeField(_('preparation time'), default=timedelta(seconds=30))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('user'))
    result = models.CharField(_('result'), max_length=24)
    created = models.TimeField(_('preparation time'), auto_now_add=True)


class Pig(models.Model):
    level = models.IntegerField(_('level'), default=1)
    status = models.CharField(_('pig status'), max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=('user'))
    upgrade_started = models.TimeField(_('upgrade started'), default=timezone.now)
    upgrade_time = models.TimeField(_('upgrade time'), default=timedelta(seconds=30), blank=True)
