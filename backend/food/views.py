from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import RecipesFilter
from .food_models import Ingredients, Products, Recipes
from .marks_models import Tags
from .serializers import (FavoriteCreateDestroySerializer,
                          IngredientsSerializer, RecipeAddSerializer,
                          RecipesSerializer,
                          ShoppingListCreateDestroySerializer, TagsSerializer)

HAS_NOT_INGREDIENT = "В базе данных нет ингредиента с id {id}"


class ListRetriveView(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    pagination_class = LimitOffsetPagination


class TagsViewSet(ListRetriveView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()
    permission_classes = [permissions.AllowAny]


class IngredientsViewSet(ListRetriveView):
    serializer_class = IngredientsSerializer
    queryset = Products.objects.all()
    permission_classes = [permissions.AllowAny]


class RecipesViewSet(ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = LimitOffsetPagination
    filterset_class = RecipesFilter
    permission_classes = [IsAdminOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(
            tags=self.request.data["tags"],
            author=self.request.user,
        )

    def create(self, request, *args, **kwargs):
        [
            get_object_or_404(Products, id=ingredient["id"])
            for ingredient in request.data["ingredients"]
        ]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        recipe_id = serializer.data["id"]
        for ingredient in request.data["ingredients"]:
            Ingredients.objects.create(
                recipe=get_object_or_404(Recipes, id=recipe_id),
                ingredient=get_object_or_404(Products, id=ingredient["id"]),
                amount=ingredient["amount"],
            )
        headers = self.get_success_headers(serializer.data)
        recipe = self.get_serializer(get_object_or_404(Recipes, id=recipe_id))
        return Response(
            recipe.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ChangeShoppingListViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = ShoppingListCreateDestroySerializer
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
    serializer_class = FavoriteCreateDestroySerializer
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


class DownloadShoppingCart(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, *args, **kwargs):
        queryset = self.request.user.buyer
        print(queryset)
