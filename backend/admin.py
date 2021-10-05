from django.contrib import admin

from backend.users.models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "username",
        "email",
        "first_name",
        "last_name",
    )
    search_fields = (
        "username",
        "email",
        "last_name",
        "first_name",
    )
    list_filter = (
        "username",
        "email",
    )
    empty_value_display = "-пусто-"


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "following",
        "follower",
    )
    search_fields = (
        "following",
        "follower",
    )
    list_filter = (
        "following",
        "follower",
    )
    empty_value_display = "-пусто-"
