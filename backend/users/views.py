from djoser.views import UserViewSet

from .serializers import CustomUserSerializer
from .models import CustomUser


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
