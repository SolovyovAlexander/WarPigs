from rest_framework import serializers

from users.models import User, Raid, Pig


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'bricks', 'rating', 'id']


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
