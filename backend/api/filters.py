from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters

from recipes.models import Recipe, Tag


class IngredientSearchFilter(rest_filters.SearchFilter):
    search_param = 'name'


class RecipeFilter(filters.FilterSet):
    author = filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact',
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='filter_related_recipes'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_related_recipes'
    )

    def filter_related_recipes(self, queryset, name, value):
        user = self.request.user
        if not user.is_authenticated or not value:
            return queryset
        elif name == 'is_favorited':
            return queryset.filter(favorite_recipe__user=user)
        return queryset.filter(recipe_to_cart__user=user)

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)
