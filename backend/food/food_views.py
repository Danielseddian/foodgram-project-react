from base64 import b64decode
from io import BytesIO
from uuid import uuid4

from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from .filters import IngredientsFilter, RecipesFilter
from .food_models import Ingredients, Products, Recipes
from .food_serializers import (GetRecipesSerializer, ProductsSerializer,
                               RecipeAddSerializer)

MISSING_AMOUNT = "Так ничего не приготовить — требуется больше ингредиента"
BASE64 = ";base64,"
WRONG_PRODUCT = "Такого ингредиента пока нет, но, возможно, скоро появится."
WRONG_IMAGE_TYPE = "Изображение не соответствует"


class IngredientsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = None
    filterset_class = IngredientsFilter
    permission_classes = [IsAdminOrReadOnly]


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.all()
    filterset_class = RecipesFilter
    permission_classes = [IsAdminOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        if "tags" not in self.request.query_params and not self.kwargs:
            return queryset.none()
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetRecipesSerializer
        try:
            image = self.request.data["image"]
            self.request.data["image"] = (
                self.get_base64_image(image) if BASE64 in image else image
            )
        except KeyError:
            None
        return RecipeAddSerializer

    def get_base64_image(self, picture):
        try:
            extantion, base = picture.split(BASE64)
            extantion = "." + extantion.split("/")[-1]
            extantion = extantion if extantion != ".jpeg" else ".jpg"
            base = BytesIO(b64decode(base))
        except TypeError:
            raise ValidationError(WRONG_IMAGE_TYPE)
        file_name = str(uuid4())[:12] + extantion
        return InMemoryUploadedFile(
            base,
            field_name="image",
            name=file_name,
            content_type="image/jpeg",
            size=len(base.getvalue()),
            charset=None,
        )

    def validate_ingredients(self, data):
        amounts = {}
        for ingredient in data:
            amount = int(ingredient["amount"])
            if amount < 1:
                raise ValidationError(MISSING_AMOUNT)
            pk = int(ingredient["id"])
            amounts[pk] = amounts[pk] + amount if pk in amounts else amount
        products = Products.objects.filter(id__in=amounts)
        values = [pk["id"] for pk in products.values("id")]
        if amounts.keys() - values:
            raise ValidationError(WRONG_PRODUCT)
        return amounts, products

    def create_or_update_ingredients(self, amounts, products, recipe):
        key = "ingredient__id"
        ingredients = Ingredients.objects.filter(recipe=recipe)
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
                ingredient = Ingredients(
                    ingredient=product,
                    recipe=recipe,
                    amount=amounts[product_id],
                )
                adding.append(ingredient)
        if updating:
            Ingredients.objects.bulk_update(updating, ["amount"])
        Ingredients.objects.bulk_create(adding) if adding else None
        ingredients.exclude(ingredient__id__in=amounts).delete()

    def create(self, request, *args, **kwargs):
        data = request.data
        amounts, products = self.validate_ingredients(data["ingredients"])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tags=request.data["tags"], author=request.user)
        recipe = Recipes.objects.get(id=serializer.data["id"])
        self.create_or_update_ingredients(amounts, products, recipe)
        headers = self.get_success_headers(serializer.data)
        recipe = self.get_serializer(recipe)
        return Response(recipe.data, status=HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipes, id=kwargs["pk"])
        self.create_or_update_ingredients(request.data["ingredients"], recipe)
        return super().update(request, *args, **kwargs)
