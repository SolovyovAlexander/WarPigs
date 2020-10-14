from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import serializers

from users.models import User, Raid, Pig
from users.tasks import precess_raid


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pigs_count = serializers.SerializerMethodField()
    raids_in_progress = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "username",
            "bricks",
            "rating",
            "pigs_count",
            "raids_in_progress",
            "id",
        ]

    @staticmethod
    def get_pigs_count(instance):
        return Pig.objects.filter(user=instance).count()

    @staticmethod
    def get_raids_in_progress(instance):
        return Raid.objects.filter(user=instance, status="in_progress")


class RaidPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid
        fields = [
            "user_to_raid",
            "status",
            "user",
        ]

    def create(self, validated_data, *args, **kwargs):
        raid = super(RaidPostSerializer, self).create(validated_data, *args, **kwargs)
        t = raid.preparation_time
        t = datetime.strptime(t, '%H:%M:%S').time()
        duration = (t.hour * 60 + t.minute) * 60 + t.second
        precess_raid.apply_async(kwargs={"raid_id": raid.id}, countdown=duration-1)
        return raid


class RaidGetSerializer(serializers.ModelSerializer):
    time_left = serializers.SerializerMethodField()

    class Meta:
        model = Raid
        fields = [
            "id",
            "user_to_raid",
            "result",
            "created",
            "preparation_time",
            "time_left",
        ]

    @staticmethod
    def get_time_left(instance):
        t = instance.preparation_time
        duration = (t.hour * 60 + t.minute) * 60 + t.second
        time_left = instance.created + timedelta(seconds=duration) - timezone.now()
        if time_left > timedelta(seconds=0):
            return str(time_left).split(".")[0]
        return False


class RaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid
        fields = "__all__"


class PigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pig
        fields = "__all__"


class PigUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pig
        fields = [
            "upgrade_time",
        ]
