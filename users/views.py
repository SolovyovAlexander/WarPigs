from rest_framework import viewsets, permissions, mixins

# Create your views here.
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User, Raid, Pig
from users.serializers import UserSerializer, RaidPostSerializer, RaidGetSerializer, RaidSerializer, PigSerializer, \
    PigUpgradeSerializer


def index_view(request):
    return render(request, "index.html", {})


def pigs_view(request):
    return render(request, "pigs.html", {})


def raids_view(request):
    return render(request, "raids.html", {})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RaidViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):

    def get_queryset(self):
        return Raid.objects.filter(user=self.kwargs.get('user_pk', ''))

    def get_serializer_class(self):
        if self.action == 'create':
            return RaidPostSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return RaidGetSerializer
        return RaidSerializer


class PigViewSet(viewsets.ModelViewSet):
    serializer_class = PigSerializer

    def get_queryset(self):
        return Pig.objects.filter(user=self.kwargs.get('user_pk')).order_by("-id")

    def create(self, request, *args, **kwargs):
        lvl = int(self.request.data.get("level", 1))
        user = User.objects.get(pk=self.kwargs.get('user_pk'))
        create_cost = lvl * 100
        if user.bricks >= create_cost:
            res = super(PigViewSet, self).create(request, *args, **kwargs)
            user.bricks -= create_cost
            user.save()
            return res
        else:
            return JsonResponse({"error": "Not enough coins!"}, status=400)

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
