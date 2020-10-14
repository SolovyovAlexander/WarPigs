from django.contrib import admin

from .models import *


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    search_fields = ("username",)


class RaidAdmin(admin.ModelAdmin):
    search_fields = ("user", "user_to_raid")


class PigAdmin(admin.ModelAdmin):
    search_fields = ("name", "user")


admin.site.register(User, UserAdmin)
admin.site.register(Raid, RaidAdmin)
admin.site.register(Pig, PigAdmin)
