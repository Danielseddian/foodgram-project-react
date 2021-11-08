from drf_extra_fields.fields import Base64ImageField
from foodgram.settings import STATIC_ROOT
from rest_framework.serializers import (CharField, ModelSerializer,
                                        SerializerMethodField)
from users.serializers import UserSerializer

from .food_models import Ingredients, Products, Recipes
from .lists_models import Favorites, ShoppingLists
from .marks_serializers import TagsSerializer


class ProductsSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Products


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
    image = SerializerMethodField()

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

    def get_image(self, obj):
        return STATIC_ROOT + obj.image.name


class RecipeAddSerializer(RecipesSerializer):
    image = Base64ImageField(max_length=None, use_url=True)

    class Meta:
        fields = ["id", "tags", "name", "image", "cooking_time", "text"]
        model = Recipes
