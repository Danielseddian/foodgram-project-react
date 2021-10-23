from rest_framework import status  # , permissions
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)

from .food_models import Ingredients, Products, Recipes
from ..users.models import User
from ..permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from .marks_models import Tags
from .serializers import (
    RecipesSerializer,
    ShoppingListCreateDestroySerializer,
    TagsSerializer,
    IngredientsSerializer,
    FavoriteCreateDestroySerializer,
)

from .filters import RecipesFilter

HAS_NOT_INGREDIENT = "В базе данных нет ингредиента с id {id}"


class ListRetriveView(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    pagination_class = PageNumberPagination
    pass


class TagsViewSet(ListRetriveView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class IngredientsViewSet(ListRetriveView):
    serializer_class = IngredientsSerializer
    queryset = Products.objects.all()


class RecipesViewSet(ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes.objects.all()
    pagination_class = PageNumberPagination
    filterset_class = RecipesFilter
    permission_classes = IsAdminOrReadOnly, IsAuthorOrReadOnly

    def perform_create(self, serializer):
        serializer.save(
            tags=self.request.data["tags"],
            author=get_object_or_404(User, id=1),
        )  # self.request.user,)

    def create(self, request, *args, **kwargs):
        [
            get_object_or_404(Products, id=ingredient["id"])
            for ingredient in request.data["ingredients"]
        ]
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        for ingredient in request.data["ingredients"]:
            Ingredients.objects.create(
                recipe=get_object_or_404(Recipes, id=serializer.data["id"]),
                ingredient=get_object_or_404(Products, id=ingredient["id"]),
                amount=ingredient["amount"],
            )
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ChangeShoppingListViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = ShoppingListCreateDestroySerializer
    # permission_classes = permissions.IsAuthenticated

    def get(self, request, *args, **kwargs):
        request.data["products"] = kwargs["shop_id"]
        request.data["buyer"] = 2  # self.request.user.id
        # data = self.create(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            get_object_or_404(
                User,
                id=2,
            ).admirer,  # self.request.user.admirer,
            recipe__id=kwargs["shop_id"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = FavoriteCreateDestroySerializer
    # permission_classes = permissions.IsAuthenticated

    def get(self, request, *args, **kwargs):
        request.data["recipe"] = kwargs["favorite_id"]
        request.data["admirer"] = 2  # self.request.user.id
        # data = self.create(request, *args, **kwargs)
        return self.create(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            get_object_or_404(
                User,
                id=2,
            ).admirer,  # self.request.user.admirer,
            recipe__id=kwargs["favorite_id"],
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
