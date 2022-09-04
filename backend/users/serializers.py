from djoser.serializers import UserSerializer
from .models import CustomUser


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name')
        # 'is_subscribed'
