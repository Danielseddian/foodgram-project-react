from rest_framework import serializers

from .lists_models import Favorite, ShoppingList

HAS_BEEN_ADDED = "Этот рецепт уже в списке"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Favorite
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=["admirer", "recipe"],
                message=HAS_BEEN_ADDED,
            )
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = ShoppingList
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingList.objects.all(),
                fields=["buyer", "products"],
                message=HAS_BEEN_ADDED,
            )
        ]
