import io

import reportlab
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCartItem, Tag)
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import filters, permissions, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.permissions import IsAuthor

from .filters import RecipeFilter
from .mixins import CreateDestroyViewSet, RetrieveViewSet
from .serializers import (IngredientSerializer, RecipeGetSerializer,
                          RecipePostSerializer, RecipeSnippetSerializer,
                          TagSerializer)

TO_UPPER_DIRECTORY = 8


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
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny, ]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated, ]
        elif self.request.method == 'PATCH' or 'DELETE':
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

    def create(self, request, Model=Favorite,
               message='Recipe already in favorites',
               *args, **kwargs):
        instance = self.get_object()
        favorite = Favorite.objects.filter(user=request.user, recipe=instance)
        if favorite:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        Favorite.objects.create(user=request.user, recipe=instance)
        serializer = RecipeSnippetSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, Model=Favorite,
                message='Recipe not in favorites',
                *args, **kwargs):
        instance = self.get_object()
        favorite = Favorite.objects.filter(user=request.user, recipe=instance)
        if favorite:
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ShoppingCartViewSet(FavoriteViewSet):

    def create(self, request, *args, **kwargs):
        return FavoriteViewSet.create(
            self, request, Model=ShoppingCartItem,
            message='Recipe already in shopping cart',
            *args, **kwargs
        )

    def destroy(self, request, *args, **kwargs):
        return FavoriteViewSet.destroy(
            self, request, Model=ShoppingCartItem,
            message='Recipe not in shopping cart',
            *args, **kwargs
        )


class DownloadShoppingList(RetrieveViewSet):
    permission_classes = [IsAuthenticated, ]

    def create_shopping_list(self, request):
        shopping_dict = {}
        recipes = (Recipe.objects.prefetch_related('ingredients')
                   .filter(recipe_to_cart__user_id=request.user.id))
        for recipe in recipes:
            ingredients = recipe.ingredients.all()
            for ingredient in ingredients:
                amount = (
                    IngredientAmount.objects
                    .filter(ingredient=ingredient, recipe=recipe)[0].amount)
                ingredient_with_measure = (str(ingredient.name) + ' / '
                                           + str(ingredient.measurement_unit))
                if ingredient_with_measure in shopping_dict:
                    shopping_dict[ingredient_with_measure] += amount
                else:
                    shopping_dict[ingredient_with_measure] = amount
        return shopping_dict

    def download_shopping_list(self, request):
        reportlab.rl_config.TTFSearchPath.append(
            str(settings.BASE_DIR)[:-TO_UPPER_DIRECTORY] + '\\data\\')
        pdfmetrics.registerFont(TTFont(
            'ClearSans', 'ClearSans-Regular.ttf'))
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        pdf.setFont(psfontname='ClearSans', size=12)
        left_margin = 100
        bottom_margin = 700

        shopping_list = self.create_shopping_list(request)
        if not shopping_list:
            pdf.drawString(left_margin - 25, bottom_margin + 40,
                           'Shopping List is empty. Add some'
                           ' recipes to shopping cart:)')
        else:
            pdf.drawString(left_margin - 25, bottom_margin + 40,
                           'Shopping List')
            for key in shopping_list:
                pdf.drawString(left_margin, bottom_margin,
                               f'{key} :   {shopping_list[key]}')
                bottom_margin -= 20
                if bottom_margin == 100:
                    bottom_margin = 700

        pdf.showPage()
        pdf.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True,
                            filename='Shopping_list.pdf')
