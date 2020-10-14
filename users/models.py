from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    bricks = models.IntegerField(_("bricks"), default=100)
    rating = models.IntegerField(_("rating"), default=0)

    def __str__(self):
        return f"{self.username} {self.email}"


class Raid(models.Model):
    user_to_raid = models.IntegerField(_("user to raid"))
    status = models.CharField(_("status"), max_length=24)
    preparation_time = models.TimeField(
        _("preparation time"), default="00:00:30", blank=True, null=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=("user"))
    result = models.CharField(_("result"), max_length=24, default="active", blank=True, null=True)
    created = models.DateTimeField(_("created"), auto_now_add=True)


class Pig(models.Model):
    name = models.CharField(default="default pig", max_length=40)
    level = models.IntegerField(_("level"), default=1)
    status = models.CharField(_("pig status"), max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pigs', verbose_name=("user"))
    upgrade_started = models.DateTimeField(_("upgrade started"), default=timezone.now, blank=True, null=True)
    upgrade_time = models.DurationField(default=timedelta(seconds=2))
