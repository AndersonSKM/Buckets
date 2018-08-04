from django.db import transaction
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
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
from accounts.services import send_user_activation_email, send_user_password_reset_email
from core.permissions import AllowAnyCreateUpdateIsOwner


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """User Views

    create:
    Create a new user instance.\n
    When a user is created successfull, an activation link is sent to the registered address\n
    *No permissions required for this action.*

    retrieve:
    Return the given user.

    delete:
    Destroy the given user.

    update:
    Update the full data of given user.

    partial_update:
    Update partial of data given.

    activate:
    Active the given user account.\n
    *No permissions required for this action.*
    """
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

    @action(methods=['POST',], detail=False, permission_classes=[AllowAny,])
    def activate(self, request):
        serializer = self._validate_request(request)
        serializer.user.activate()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST',], detail=False, permission_classes=[AllowAny,],
            url_path='password-forgot')
    def password_forgot(self, request):
        serializer = self._validate_request(request)
        try:
            send_user_password_reset_email(serializer.user)
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            raise APIException({'detail': str(error)})

    @action(methods=['POST',], detail=False, permission_classes=[AllowAny,],
            url_path='password-reset')
    def password_reset(self, request):
        self._process_change_password(request)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST',], detail=False, url_path='change-password')
    def change_password(self, request):
        self._process_change_password(request)
        return Response(status=status.HTTP_200_OK)

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save()
        try:
            send_user_activation_email(instance)
        except Exception as error:
            raise APIException({'detail': str(error)})

    def _validate_request(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer

    def _process_change_password(self, request):
        serializer = self._validate_request(request)
        serializer.user.set_password(serializer.validated_data['password'])
        serializer.user.save()
