from django.contrib import admin

from .models import (Tag, Ingredient, IngredientAmount, Recipe, Favorite,
                     Favorite, ShoppingCartItem)

admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientAmount)
admin.site.register(Recipe)
admin.site.register(Favorite)
admin.site.register(ShoppingCartItem)
