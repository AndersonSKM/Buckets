from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import (
    UserActivateSerializer,
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserPasswordForgotSerializer,
    UserPasswordResetSerializer,
    UserSerializer,
)
from core.permissions import AllowAnyCreateUpdateIsOwner


class UserViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,
                  mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAnyCreateUpdateIsOwner,)

    def get_serializer_class(self):
        serializers = {
            'create': UserCreateSerializer,
            'activate': UserActivateSerializer,
            'password_forgot': UserPasswordForgotSerializer,
            'password_reset': UserPasswordResetSerializer,
            'change_password': UserChangePasswordSerializer,
        }
        return serializers.get(self.action, UserSerializer)

    def get_permissions(self):
        if self.action in ['activate', 'password_forgot', 'password_reset']:
            return [AllowAny(),]
        return super().get_permissions()

    @action(methods=['POST',], detail=False)
    def activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        User.objects.activate(user=serializer.validated_data['user'])
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST',], detail=False, url_path='password-forgot')
    def password_forgot(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        User.objects.send_password_reset_email(user=serializer.validated_data['user'])
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST',], detail=False, url_path='password-reset')
    def password_reset(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        User.objects.update_password(
            user=data['user'],
            password=data['password'],
            confirm=data['password_confirm']
        )
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST',], detail=False, url_path='change-password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        User.objects.change_current_password(
            user=request.user,
            current_password=data['current_password'],
            password=data['password'],
            confirm=data['password_confirm']
        )
        return Response(status=status.HTTP_200_OK)
