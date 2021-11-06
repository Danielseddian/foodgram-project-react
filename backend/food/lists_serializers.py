from rest_framework import serializers

from .lists_models import Favorites, ShoppingLists

HAS_BEEN_ADDED = "Этот рецепт уже в списке"


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Favorites
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Favorites.objects.all(),
                fields=["admirer", "recipe"],
                message=HAS_BEEN_ADDED,
            )
        ]


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = ShoppingLists
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=ShoppingLists.objects.all(),
                fields=["buyer", "products"],
                message=HAS_BEEN_ADDED,
            )
        ]
