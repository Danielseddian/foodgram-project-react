from rest_framework.serializers import (CharField, ModelSerializer,
                                        SerializerMethodField)

from .converters import Base64ImageField
from .food_models import Ingredient, Product, Recipe
from .lists_models import Favorite, ShoppingList
from .marks_models import Tag
from .marks_serializers import TagSerializer
from .validators import validate_ingredients, validate_tags, validate_time
from api.users.serializers import UserSerializer


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


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = SerializerMethodField("check_is_favorite")
    is_in_shopping_cart = SerializerMethodField("check_is_in_shopping_cart")
    image = Base64ImageField()

    class Meta:
        fields = "__all__"
        model = Recipe

    def validate_cooking_time(self, cooking_time):
        validate_time(cooking_time)
        return super().validate(cooking_time)

    def validate_tags(self, tags):
        validate_tags(tags)
        return super().validate(tags)

    def check_is_favorite(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        admirer = request.user
        favorited = (
            True
            if admirer.is_authenticated
            and Favorite.objects.filter(
                recipe=obj.id,
                admirer=admirer.id,
            ).exists()
            else False
        )
        return favorited

    def check_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        buyer = request.user
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

    def create(self, data):
        tags = data.pop("tags")
        amounts, products = validate_ingredients(data.pop("ingredients"))
        recipe = Recipe.objects.create(**data)
        self.fill_the_recipe(amounts, products, recipe, tags)
        return recipe

    def update(self, recipe, data):
        tags = data.pop("tags")
        amounts, products = validate_ingredients(data.pop("ingredients"))
        self.fill_the_recipe(amounts, products, recipe, tags)
        super().update(recipe, data)
        return recipe

    def fill_the_recipe(self, amounts, products, recipe, tags):
        recipe.tags.set(Tag.objects.filter(id__in=tags))
        key = "ingredient__id"
        ingredients = Ingredient.objects.filter(recipe=recipe)
        values = [pk[key] for pk in ingredients.values(key)]
        adding = []
        updating = []
        for product in products:
            product_id = product.id
            if product_id in values:
                ingredient = ingredients.get(ingredient__id=product_id)
                ingredient.amount = amounts[product_id]
                updating.append(ingredient)
            else:
                ingredient = Ingredient(
                    ingredient=product,
                    recipe=recipe,
                    amount=amounts[product_id],
                )
                adding.append(ingredient)
        if updating:
            Ingredient.objects.bulk_update(updating, ["amount"])
        if adding:
            Ingredient.objects.bulk_create(adding)
        ingredients.exclude(ingredient__id__in=amounts).delete()

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data["image"] = obj.image.url
        return data
