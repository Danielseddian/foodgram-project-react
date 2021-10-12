from django.contrib import admin

from backend.users.models import User, Follow
from backend.food.food_models import Ingredients, Products, Recipes
from backend.food.lists_models import ShoppingLists, Favorites
from backend.food.marks_models import Tags


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


@admin.register(Favorites)
class FavoritesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "admirer",
        "recipe",
    )
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = "-пусто-"


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "ingredient",
        "amount",
        "recipe",
    )
    search_fields = (
        "ingredient",
        "amount",
        "recipe",
    )
    list_filter = (
        "ingredient",
        "amount",
        "recipe",
    )
    empty_value_display = "-пусто-"


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "measurement_unit",
    )
    search_fields = ("name",)
    list_filter = (
        "name",
        "measurement_unit",
    )
    empty_value_display = "-пусто-"


@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "name",
        "image",
        "text",
        "cooking_time",
    )
    search_fields = ()
    list_filter = ()
    empty_value_display = "-пусто-"


@admin.register(ShoppingLists)
class ShoppingListsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "buyer",
        "product",
    )
    search_fields = (
        "buyer",
        "product",
    )
    list_filter = (
        "buyer",
        "product",
    )
    empty_value_display = "-пусто-"


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "color",
        "slug",
    )
    search_fields = (
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "color",
        "slug",
    )
    empty_value_display = "-пусто-"
