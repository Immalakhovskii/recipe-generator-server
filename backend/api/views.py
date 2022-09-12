from rest_framework import viewsets, filters, permissions
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .mixins import CreateDestroyViewSet
from users.permissions import IsAuthor
from recipes.models import (Tag, Ingredient, Recipe, IngredientAmount,
                            Favorite, ShoppingCartItem)
from .serializers import (
    TagSerializer, IngredientSerializer, RecipeGetSerializer,
    RecipePostSerializer, RecipeSnippetSerializer)


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

    def get_permissions(self):
        if self.request.method == 'PATCH' or 'DELETE':
            self.permission_classes = [IsAuthor, ]
        return super(RecipeViewSet, self).get_permissions()

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

    def perform_update(self, serializer):
        data = serializer.validated_data
        ingredients = data.pop('ingredients')
        tags = data.pop('tags')
        instance = serializer.save()
        if ingredients:
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if tags:
            instance.tags.set(tags)
        instance.tags.clear()


class FavoriteViewSet(CreateDestroyViewSet):

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs['recipe_id'])

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        favorite = Favorite.objects.filter(user=request.user, recipe=instance)
        if favorite.exists():
            return Response('Recipe already in favorites',
                            status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe=instance)
        serializer = RecipeSnippetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        favorite = Favorite.objects.filter(user=request.user, recipe=instance)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Recipe not in favorites',
                        status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(CreateDestroyViewSet):

    def get_object(self):
        return get_object_or_404(Recipe, id=self.kwargs['recipe_id'])

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        cart_item = (ShoppingCartItem.objects.filter(
                     user=request.user, recipe=instance))
        if cart_item.exists():
            return Response('Recipe already in shopping cart',
                            status=status.HTTP_400_BAD_REQUEST)
        ShoppingCartItem.objects.create(user=request.user, recipe=instance)
        serializer = RecipeSnippetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cart_item = (ShoppingCartItem.objects.filter(
                     user=request.user, recipe=instance))
        if cart_item.exists():
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Recipe not in shopping cart',
                        status=status.HTTP_400_BAD_REQUEST)


class DownloadShoppingCart(viewsets.ModelViewSet):
    pass  # Parent class to change
