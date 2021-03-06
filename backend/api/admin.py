from django.contrib import admin

from .food.food_models import Ingredient, Product, Recipe
from .food.lists_models import Favorite, ShoppingList
from .food.marks_models import Tag
from .users.models import Follow, User


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


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "admirer",
        "recipe",
    )
    search_fields = ("recipe",)
    list_filter = ("recipe",)
    empty_value_display = "-пусто-"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
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


class IngredientInLine(admin.TabularInline):
    model = Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "author",
        "name",
        "image",
        "text",
        "cooking_time",
    )
    inlines = [IngredientInLine]
    search_fields = ("author", "name", "tags")
    list_filter = ("author", "name", "tags")
    empty_value_display = "-пусто-"

    def save_model(self, request, obj, form, change):
        image_name, image_format = str(obj.image).split(".")
        obj.image.name = str(obj.name) + "." + image_format
        return super().save_model(request, obj, form, change)


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "buyer",
        "products",
    )
    search_fields = (
        "buyer",
        "products",
    )
    list_filter = (
        "buyer",
        "products",
    )
    empty_value_display = "-пусто-"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
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
