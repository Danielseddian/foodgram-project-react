from rest_framework import serializers

from .marks_models import Tags
from .lists_models import Favorites, ShoppingLists
from .food_models import Products, Recipes
from ..users.serializers import UserSerializer

HAS_FAVORITED = "Этот рецепт уже в избранном"
HAS_BEEN_ADDED = "Этот продукт уже в списке покупок"


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Tags


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Products


class FavoriteCreateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Favorites
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorites.objects.all(),
                fields=["admirer", "recipe"],
                message=HAS_FAVORITED,
            )
        ]


class ShoppingListCreateDestroySerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = ShoppingLists
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingLists.objects.all(),
                fields=["buyer", "products"],
                message=HAS_FAVORITED,
            )
        ]


class RecipesSerializer(serializers.ModelSerializer):
    Tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientsSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField("get_user_favorite")
    is_in_shopping_cart = serializers.SerializerMethodField(
        "get_user_shopping_cart",
    )

    class Meta:
        fields = "__all__"
        model = Recipes

    def get_user_favorite(self, obj):
        admirer = self.context["request"].user
        favorite = (
            True
            if admirer.is_authenticated
            and Favorites.objects.filter(
                recipe=obj,
                admirer=admirer,
            )
            else False
        )
        return favorite

    def get_user_shopping_cart(self, obj):
        buyer = self.context["request"].user
        is_in_shopping_cart = (
            True
            if buyer.is_authenticated
            and ShoppingLists.objects.filter(
                recipe=obj,
                admirer=buyer,
            )
            else False
        )
        return is_in_shopping_cart
