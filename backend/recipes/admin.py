from django.contrib import admin

from .forms import AtLeastOneFormSet
from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCartItem, Tag)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 2
    formset = AtLeastOneFormSet


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count',)
    search_fields = ('name', 'author__username', 'tags__name',)
    inlines = [IngredientInline, ]
    filter_horizontal = ('tags',)

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    search_fields = ('name',)


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCartItem)
