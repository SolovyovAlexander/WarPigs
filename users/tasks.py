from celery import shared_task

from users.models import User


@shared_task
def increase_bricks_number():
    for user in User.objects.all():
        user.bricks+=100
        user.save()
