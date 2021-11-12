from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from base64 import b64decode
from uuid import uuid4
from os.path import join
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from foodgram.settings import MEDIA_ROOT
from django.db.models.query import QuerySet
from django.http import FileResponse
from django_filters import rest_framework as rest_filters
from rest_framework import permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import RecipesFilter
from .food_models import Ingredients, Products, Recipes
from .food_serializers import (GetRecipesSerializer, ProductsSerializer,
                               RecipeAddSerializer)
from .lists_serializers import FavoriteSerializer, ShoppingListSerializer
from .marks_models import Tags
from .marks_serializers import TagsSerializer

BASE64 = ";base64,"
HAS_NOT_INGREDIENT = "В базе данных нет ингредиента с id {id}"


class ListRetriveView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pass


class TagsViewSet(ListRetriveView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    pagination_class = None
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_fields = ["name", "slug"]
    permission_classes = [permissions.AllowAny]


class IngredientsViewSet(ListRetriveView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    pagination_class = None
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_fields = ["name"]
    permission_classes = [permissions.AllowAny]


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
        image = self.request.data["image"]
        if BASE64 in image:
            self.request.data[u"image"] = self.get_image_from_base64(image)
        return RecipeAddSerializer

    def get_image_from_base64(self, picture):
        try:
            extantion, base = picture.split(BASE64)
            extantion = "." + extantion.split("/")[-1]
            extantion = extantion if extantion != ".jpeg" else ".jpg"
            base = BytesIO(b64decode(base))
        except TypeError:
            raise("Изображение не соответствует")
        file_name = join(MEDIA_ROOT, str(uuid4())[:12] + extantion)
        return InMemoryUploadedFile(
            base,
            field_name="image",
            name=file_name,
            content_type="image/jpeg",
            size=len(base.getvalue()),
            charset=None,
        )

    def create(self, request, *args, **kwargs):
        ingredients = {}
        for ingredient in request.data["ingredients"]:
            product = get_object_or_404(Products, id=ingredient["id"])
            amount = ingredient["amount"]
            if product in ingredients:
                ingredients[product] += amount
            else:
                ingredients[product] = amount
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(
            tags=self.request.data["tags"],
            author=self.request.user,
        )
        recipe = get_object_or_404(Recipes, id=serializer.data["id"])
        for ingredient in ingredients:
            amount = ingredients[ingredient]
            Ingredients.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount,
            )
        headers = self.get_success_headers(serializer.data)
        recipe = self.get_serializer(recipe)
        return Response(
            recipe.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ChangeShoppingListViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = ShoppingListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs["recipe_id"]
        instance = get_object_or_404(Recipes, id=recipe_id)
        self.check_object_permissions(self.request, instance)
        serializer = self.get_view_serializer(instance)
        request.data["products"] = recipe_id
        request.data["buyer"] = self.request.user.id
        self.create(request, *args, **kwargs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_view_serializer(self, *args, **kwargs):
        serializer_class = RecipeAddSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            self.request.user.buyer,
            products__id=kwargs["recipe_id"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs["recipe_id"]
        instance = get_object_or_404(Recipes, id=recipe_id)
        self.check_object_permissions(self.request, instance)
        serializer = self.get_view_serializer(instance)
        request.data["recipe"] = recipe_id
        request.data["admirer"] = self.request.user.id
        self.create(request, *args, **kwargs)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_view_serializer(self, *args, **kwargs):
        serializer_class = RecipeAddSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            self.request.user.admirer,
            recipe__id=kwargs["recipe_id"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCart(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        name = "products__ingredients__ingredient__name"
        measurement = "products__ingredients__ingredient__measurement_unit"
        amount = "products__ingredients__amount"
        ingredients = self.request.user.buyer.values(name, measurement, amount)
        products = {}
        for ingredient in ingredients:
            name, measurement, amount = ingredient.values()
            product = name + f" ({measurement}) — "
            if product in products:
                products[product] += amount
            else:
                products[product] = amount
        file_path = "shopping_cart.txt"
        with open(file_path, "w") as cart:
            for product in products:
                cart.write(product + str(products[product]) + "\n")
        return FileResponse(open(file_path, "rb"))
