from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from users.views import index_view
from users.views import pigs_view
from users.views import raids_view
from users.views import UserViewSet, RaidViewSet, PigViewSet

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")

raid_router = NestedSimpleRouter(router, r"users", lookup="user")
raid_router.register(r"raids", RaidViewSet, basename="user-raid")

pig_router = NestedSimpleRouter(router, r"users", lookup="user")
pig_router.register(r"pigs", PigViewSet, basename="user-raid")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(raid_router.urls)),
    path("", include(pig_router.urls)),
    path("", index_view, name="index_view"),
    path("pigs", pigs_view, name="pigs_view"),
    path("raids", raids_view, name="raids_view"),
]
