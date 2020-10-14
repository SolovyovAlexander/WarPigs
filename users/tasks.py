from datetime import timedelta

from celery import shared_task

from users.models import User, Pig, Raid


@shared_task
def increase_bricks_number():
    for user in User.objects.all():
        user.bricks += 100
        user.save()


@shared_task
def upgrade_pig(pig_id):
    pig = Pig.objects.get(id=pig_id)
    pig.level += 1
    # pow(2, N) seconds
    pig.upgrade_time = timedelta(seconds=pow(2, pig.level))
    pig.upgrade_cost = int(50 * pig.level)
    pig.status = "idle"
    pig.save()


@shared_task
def precess_raid(raid_id):
    raid = Raid.objects.get(id=raid_id)
    attacker = raid.user
    defender = User.objects.get(id=raid.user_to_raid)

    raid.status = "Defeated"

    if attacker.pigs.count() > defender.pigs.count():
        bricks_stolen = sum(attacker.pigs.all().values_list("level", flat=True)) * 50
        bricks_stolen = min(bricks_stolen, defender.bricks)
        defender.bricks -= bricks_stolen
        attacker.bricks += bricks_stolen
        raid.status = f"Victory! {bricks_stolen} bricks stolen!"

    defender.save()
    attacker.save()
    raid.save()
