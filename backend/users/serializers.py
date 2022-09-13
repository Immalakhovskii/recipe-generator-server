from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import CustomUser, Subscription


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'password')


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            subscriber=request.user, subscription=obj).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_is_subscribed(self, obj):
        return CustomUserSerializer.get_is_subscribed(self, obj)

    def get_recipes_count(self, obj):
        return obj.author.all().count()

    def get_recipes(self, obj):
        from api.serializers import RecipeSnippetSerializer
        recipes_limit = (self.context['request']
                         .query_params.get('recipes_limit'))
        if recipes_limit:
            return RecipeSnippetSerializer(
                instance=obj.author.all()[:int(recipes_limit)],
                many=True).data
        instance = obj.author.all()
        return RecipeSnippetSerializer(
            instance=instance,
            many=True).data
