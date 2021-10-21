from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)

from .food_models import Products, Recipes
from ..users.models import User

# from .lists_models import Favorites
from .marks_models import Tags
from .serializers import (
    RecipesSerializer,
    ShoppingListCreateDestroySerializer,
    TagsSerializer,
    IngredientsSerializer,
    FavoriteCreateDestroySerializer,
)


class ListRetriveView(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    pass


class TagsViewSet(ListRetriveView):
    serializer_class = TagsSerializer
    queryset = Tags.objects.all()


class IngredientsViewSet(ListRetriveView):
    serializer_class = IngredientsSerializer
    queryset = Products.objects.all()


class RecipesViewSet(ModelViewSet):
    serializer_class = RecipesSerializer
    queryset = Recipes


class ChangeShoppingListViewSet(GenericViewSet, CreateModelMixin):
    serializer_class = ShoppingListCreateDestroySerializer

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
