from django_filters import rest_framework as filters
from django_filters.filters import (AllValuesFilter, AllValuesMultipleFilter,
                                    CharFilter)

from .food_models import Product, Recipe


class RecipeFilter(filters.FilterSet):
    author = AllValuesFilter(
        method="get_user_recipes",
    )
    tags = AllValuesMultipleFilter(
        method="get_tagged_recipes",
        field_name="tags__slug",
    )
    is_favorited = filters.BooleanFilter(method="get_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_shopping_cart")

    class Meta:
        model = Recipe
        fields = ["author", "tags", "is_favorited", "is_in_shopping_cart"]

    def get_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(favorited__admirer=self.request.user)
        return queryset

    def get_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Recipe.objects.filter(to_buy__buyer=self.request.user)
        return queryset

    def get_tagged_recipes(self, queryset, name, tags):
        return queryset.filter(tags__slug__in=tags).distinct("pk")

    def get_user_recipes(self, queryset, name, pk):
        return queryset.filter(author__id__in=pk)


class IngredientFilter(filters.FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Product
        fields = ("name",)
