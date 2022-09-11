from django.contrib import admin

from .forms import AtLeastOneFormSet
from .models import (Tag, Ingredient, IngredientAmount, Recipe, Favorite,
                     Favorite, ShoppingCartItem)


class IngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    formset = AtLeastOneFormSet


class RecipeAdmin(admin.ModelAdmin):
    inlines = [IngredientInline, ]
    filter_horizontal = ('tags',)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCartItem)
