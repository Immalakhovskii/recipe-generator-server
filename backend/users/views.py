from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == self.request.user:
            serializer = CustomUserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
