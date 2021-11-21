from django.db.models.query import QuerySet
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly

from .filters import IngredientFilter, RecipeFilter
from .food_models import Product, Recipe
from .food_serializers import RecipeSerializer, ProductSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    permission_classes = [IsAdminOrReadOnly]


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    filterset_class = RecipeFilter
    serializer_class = RecipeSerializer
    permission_classes = [IsAdminOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = self.queryset
        if "tags" not in self.request.query_params and not self.kwargs:
            return queryset.none()
        if isinstance(queryset, QuerySet):
            queryset = queryset.all()
        return queryset

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data["tags"],
            ingredients=self.request.data["ingredients"],
        )

    def perform_update(self, serializer):
        serializer.save(
            author=self.request.user,
            tags=self.request.data['tags'],
            ingredients=self.request.data['ingredients']
        )
