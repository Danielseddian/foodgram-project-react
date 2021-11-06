from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (CharField, ModelSerializer,
                                        SerializerMethodField)

from users.serializers import UserSerializer

from .food_models import Ingredients, Recipes
from .lists_models import Favorites, ShoppingLists
from .marks_serializers import TagsSerializer


class IngredientSerializer(ModelSerializer):
    name = CharField(read_only=True, source="ingredient.name")
    measurement_unit = CharField(
        read_only=True,
        source="ingredient.measurement_unit",
    )

    class Meta:
        fields = (
            "id",
            "name",
            "measurement_unit",
            "amount",
        )
        model = Ingredients


class RecipesSerializer(ModelSerializer):
    tags = TagsSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField("check_is_user_favorite")
    is_in_shopping_cart = SerializerMethodField("check_in_user_shopping_cart")
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        fields = "__all__"
        model = Recipes

    def check_is_user_favorite(self, obj):
        admirer = self.context["request"].user
        favorite = (
            True
            if admirer.is_authenticated
            and Favorites.objects.filter(
                recipe=obj.id,
                admirer=admirer.id,
            )
            else False
        )
        return favorite

    def check_in_user_shopping_cart(self, obj):
        buyer = self.context["request"].user
        is_in_shopping_cart = (
            True
            if buyer.is_authenticated
            and ShoppingLists.objects.filter(
                products=obj.id,
                buyer=buyer.id,
            )
            else False
        )
        return is_in_shopping_cart


class RecipeAddedSerializer(ModelSerializer):
    class Meta:
        fields = ["id", "name", "image", "cooking_time"]
        model = Recipes
