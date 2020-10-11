from rest_framework import serializers

from users.models import User, Raid, Pig


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    pigs_count = serializers.SerializerMethodField()
    raids_in_progress = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'bricks', 'rating', 'pigs_count', 'raids_in_progress', 'id']

    @staticmethod
    def get_pigs_count(instance):
        return Pig.objects.filter(user=instance).count()

    @staticmethod
    def get_raids_in_progress(instance):
        return Raid.objects.filter(user=instance, status='in_progress')


class RaidPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid
        fields = ['user_to_raid', ]


class RaidGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid
        fields = ['id', 'result', 'created']


class RaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Raid
        fields = '__all__'


class PigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pig
        fields = '__all__'


class PigUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pig
        fields = ['upgrade_time', ]
