from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import (
    FullUserCreateSerializer,
    FullUserSerializer,
    UserActivateSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from accounts.services import send_user_activation_email
from core.permissions import AllowAnyCreateUpdateIsAdminOrOwner, AllowListIsAdmin


class UserViewSet(viewsets.ModelViewSet):
    """User Views

    retrieve:
    Return the given user.

    list:
    Return a list of all the existing.\n
    *Only works if you have staff permissions.*

    create:
    Create a new user instance.\n
    When a user is created successfull,
     an activation link is sent to the registered address\n
    *No permissions required for this action.*

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
    permission_classes = (AllowAnyCreateUpdateIsAdminOrOwner, AllowListIsAdmin,)

    @action(methods=['POST',], detail=False, permission_classes=[AllowAny,])
    def activate(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        user.activate()
        return Response(status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'activate':
            return UserActivateSerializer

        if self.action == 'create':
            if self.request and self.request.user.is_staff:
                return FullUserCreateSerializer
            return UserCreateSerializer

        if self.request and self.request.user.is_staff:
            return FullUserSerializer
        return UserSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        try:
            instance = serializer.save()
            send_user_activation_email(instance)
        except Exception as error:
            raise APIException(str(error))
