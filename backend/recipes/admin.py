from django.contrib import admin

from .models import (Tag, Ingredient, IngredientAmount, Recipe, Favorite,
                     Favorite, ShoppingCartItem)


class RecipeAdmin(admin.ModelAdmin):
    filter_horizontal = ('tags',)


admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite)
admin.site.register(ShoppingCartItem)
