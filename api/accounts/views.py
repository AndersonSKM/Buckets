from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.serializers import (
    FullUserCreateSerializer,
    FullUserSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from accounts.services import UserService
from core.permissions import (
    AllowAnyCreateUpdateIsAdminOrOwner,
    AllowListIsAdmin,
)

User = get_user_model()

USER_ACTIVATE_URL = (
    'activate/'
    '(?P<uuidb64>[0-9A-Za-z_\-]+)/'
    '(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})'
)


class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given user.

    list:
    Return a list of all the existing.\n
    *Only works if you have staff permissions.*

    create:
    Create a new user instance.\n
    When a user is created successfull, an activation link is sent to the registered address\n
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
    permission_classes = (
        AllowAnyCreateUpdateIsAdminOrOwner,
        AllowListIsAdmin,
    )

    @action(methods=['get'], detail=False, permission_classes=[AllowAny],
            url_path=USER_ACTIVATE_URL)
    def activate(self, request, uuidb64=None, token=None):
        try:
            UserService.activate(uuidb64, token)
            return Response(status=status.HTTP_200_OK)
        except Exception as error:
            content = {'detail': str(error)}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        if self.action == 'create':
            if self.request and self.request.user.is_staff:
                return FullUserCreateSerializer
            return UserCreateSerializer

        if self.request and self.request.user.is_staff:
            return FullUserSerializer
        return UserSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        instance = serializer.save()
        UserService.send_activation_email(instance, self.request)
