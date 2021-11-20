from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (CharField, ImageField, ModelSerializer,
                                        SerializerMethodField)
from api.users.serializers import UserSerializer

from .food_models import Ingredient, Product, Recipe
from .lists_models import Favorite, ShoppingList
from .marks_serializers import TagSerializer

LITTLE_TIME = "На всё требуется время. Хотя бы одна минута"


class ProductSerializer(ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Product


class IngredientSerializer(ModelSerializer):
    id = CharField(read_only=True, source="ingredient.id")
    name = CharField(read_only=True, source="ingredient.name")
    measurement_unit = CharField(
        read_only=True,
        source="ingredient.measurement_unit",
    )

    class Meta:
        fields = "__all__"
        model = Ingredient


class GetRecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField("check_is_favorite")
    is_in_shopping_cart = SerializerMethodField("check_is_in_shopping_cart")
    image = SerializerMethodField()

    class Meta:
        fields = "__all__"
        model = Recipe

    def check_is_favorite(self, obj):
        admirer = self.context.get("request").user
        favorite = (
            True
            if admirer.is_authenticated
            and Favorite.objects.filter(
                recipe=obj.id,
                admirer=admirer.id,
            ).exists()
            else False
        )
        return favorite

    def check_is_in_shopping_cart(self, obj):
        buyer = self.context.get("request").user
        is_in_shopping_cart = (
            True
            if buyer.is_authenticated
            and ShoppingList.objects.filter(
                products=obj.id,
                buyer=buyer.id,
            ).exists()
            else False
        )
        return is_in_shopping_cart

    def get_image(self, obj):
        return obj.image.url


class RecipeAddSerializer(GetRecipeSerializer):
    author = UserSerializer(read_only=True)
    image = ImageField()

    class Meta:
        fields = "__all__"
        model = Recipe

    def validate(self, data):
        context = self.context.get("request")
        if int(context.data.get("cooking_time")) < 1:
            raise ValidationError(LITTLE_TIME)
        return super().validate(data)
