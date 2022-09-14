from api.views import (DownloadShoppingList, FavoriteViewSet,
                       IngredientViewSet, RecipeViewSet, ShoppingCartViewSet,
                       TagViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CustomUserViewSet, SubscriptionViewSet

app_name = 'api'
router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='users')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('recipes/<int:recipe_id>/favorite/',
         FavoriteViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='favorites'),
    path('recipes/download_shopping_cart/',
         DownloadShoppingList.as_view({'get': 'download_shopping_list'}),
         name='download_cart'),
    path('recipes/<int:recipe_id>/shopping_cart/',
         ShoppingCartViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='cart'),
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path('users/<int:user_id>/subscribe/',
         SubscriptionViewSet.as_view({'post': 'create', 'delete': 'destroy'}),
         name='subscriptions'),
    path(r'auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
