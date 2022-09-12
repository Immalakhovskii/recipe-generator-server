from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet
from api.views import (TagViewSet, IngredientViewSet, RecipeViewSet,
                       FavoriteViewSet, ShoppingCartViewSet)

app_name = 'api'
router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='favorites'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='cart')
]
