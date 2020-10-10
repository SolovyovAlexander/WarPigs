from rest_framework import viewsets, permissions, mixins

# Create your views here.
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import Raid, Pig
from users.serializers import UserSerializer, RaidPostSerializer, RaidGetSerializer, RaidSerializer, PigSerializer, \
    PigUpgradeSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer


class RaidViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        return Raid.objects.filter(user=self.kwargs.get('user_id', ''))

    def get_serializer_class(self):
        if self.action == 'create':
            return RaidPostSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return RaidGetSerializer
        return RaidSerializer


class PigViewSet(viewsets.ModelViewSet):
    serializer_class = PigSerializer

    def get_queryset(self):
        return Pig.objects.filter(user=self.kwargs.get('user_id', ''))

    @action(detail=True, methods=['patch'], serializer_class=PigUpgradeSerializer)
    def upgrade(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
