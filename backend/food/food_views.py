from base64 import b64decode
from io import BytesIO
from uuid import uuid4

from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.query import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import IngredientsFilter, RecipesFilter
from .food_models import Ingredients, Products, Recipes
from .food_serializers import (GetRecipesSerializer, ProductsSerializer,
                               RecipeAddSerializer)

BASE64 = ";base64,"


class ListRetriveView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass


class IngredientsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = None
    filterset_class = IngredientsFilter
    permission_classes = [IsAdminOrReadOnly]


class RecipesViewSet(ModelViewSet):
    queryset = Recipes.objects.none()
    filterset_class = RecipesFilter
    permission_classes = [IsAdminOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        if self.kwargs:
            return Recipes.objects.all()
        queryset = self.queryset
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
            raise ("Изображение не соответствует")
        file_name = str(uuid4())[:12] + extantion
        return InMemoryUploadedFile(
            base,
            field_name="image",
            name=file_name,
            content_type="image/jpeg",
            size=len(base.getvalue()),
            charset=None,
        )

    def create_or_update_ingredients(self, ingredients_request, recipe):
        amounts = {}
        for ingredient in ingredients_request:
            pk = int(ingredient["id"])
            amount = int(ingredient["amount"])
            amounts[pk] = amounts[pk] + amount if pk in amounts else amount
        key = "ingredient__id"
        ingredients = Ingredients.objects.filter(recipe=recipe)
        values = [pk[key] for pk in ingredients.values(key)]
        adding = []
        updating = []
        for product in Products.objects.filter(id__in=amounts):
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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(tags=request.data["tags"], author=request.user)
        recipe = Recipes.objects.get(id=serializer.data["id"])
        self.create_or_update_ingredients(request.data["ingredients"], recipe)
        headers = self.get_success_headers(serializer.data)
        recipe = self.get_serializer(recipe)
        return Response(recipe.data, status=HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipes, id=kwargs["pk"])
        self.create_or_update_ingredients(request.data["ingredients"], recipe)
        return super().update(request, *args, **kwargs)
