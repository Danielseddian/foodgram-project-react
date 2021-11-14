from django.http import FileResponse
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .food_models import Recipes
from .food_serializers import RecipeAddSerializer
from .lists_serializers import FavoriteSerializer, ShoppingListSerializer


class CreateView(GenericViewSet, CreateModelMixin):
    pass


class ChangeShoppingListViewSet(CreateView):
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
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_view_serializer(self, *args, **kwargs):
        serializer_class = RecipeAddSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            self.request.user.buyer,
            products__id=kwargs["recipe_id"],
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class FavoriteViewSet(CreateView):
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
        return Response(serializer.data, status=HTTP_201_CREATED)

    def get_view_serializer(self, *args, **kwargs):
        serializer_class = RecipeAddSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    def delete(self, *args, **kwargs):
        get_object_or_404(
            self.request.user.admirer,
            recipe__id=kwargs["recipe_id"],
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)


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
