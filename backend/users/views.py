from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet

from .models import Subscription, CustomUser
from .serializers import CustomUserSerializer, SubscriptionSerializer
from api.mixins import ListCreateDestroyViewSet


class CustomUserViewSet(UserViewSet):

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == self.request.user:
            serializer = CustomUserSerializer(self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(
            instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionViewSet(ListCreateDestroyViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return get_object_or_404(CustomUser, id=self.kwargs['user_id'])

    def list(self, request, *args, **kwargs):
        queryset = request.user.subscriber.all()
        subscriptions_queryset = []
        if queryset:
            for query in queryset:
                subscriptions_queryset.append(query.subscription)

        page = self.paginate_queryset(subscriptions_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(subscriptions_queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        subscribtion = Subscription.objects.filter(
            subscriber=request.user, subscription=instance)
        if subscribtion:
            return Response('Author already subscribed',
                            status=status.HTTP_400_BAD_REQUEST)
        Subscription.objects.create(
            subscriber=request.user, subscription=instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        subscribtion = Subscription.objects.filter(
            subscriber=request.user, subscription=instance)
        if subscribtion:
            subscribtion.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response('Author not in subscriptions',
                        status=status.HTTP_400_BAD_REQUEST)
