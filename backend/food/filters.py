from django_filters import rest_framework as filters
from django_filters.filters import AllValuesMultipleFilter

from .food_models import Recipes


class RecipesFilter(filters.FilterSet):
    tags = AllValuesMultipleFilter(
        method="get_taged_recipes",
        field_name="tags__slug",
    )
    is_favorited = filters.BooleanFilter(method="get_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_shopping_cart")

    class Meta:
        model = Recipes
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def get_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorite__admirer=self.request.user)
        return queryset

    def get_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Recipes.objects.filter(buying__buyer=self.request.user)
        return queryset

    def get_taged_recipes(self, queryset, name, values):
        if values:
            return Recipes.objects.filter(tags__slug__in=values).distinct("pk")
