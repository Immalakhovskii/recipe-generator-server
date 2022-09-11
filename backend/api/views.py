from rest_framework import viewsets, filters, permissions

from recipes.models import Tag, Ingredient, Recipe, IngredientAmount
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeGetSerializer,
    RecipePostSerializer
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeGetSerializer
        return RecipePostSerializer

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            amount = ingredient['amount']
            IngredientAmount.objects.bulk_create(
                [IngredientAmount(
                    ingredient=ingredient_id,
                    recipe=recipe, amount=amount
                )]
            )

    def perform_create(self, serializer):
        author = self.request.user
        ingredients = serializer.validated_data.pop('ingredients')
        recipe = serializer.save(author=author)
        self.create_ingredients(ingredients, recipe)
