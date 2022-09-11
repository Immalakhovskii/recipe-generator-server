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
