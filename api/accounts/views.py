from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from accounts import serializers
from core import permissions

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    retrieve:
    Return the given user.

    list:
    Return a list of all the existing.\n
    *Only works if you have staff permissions.*

    create:
    Create a new user instance.\n
    *No permissions required for this action.*

    delete:
    Destroy the given user.

    update:
    Update the full data of given user.

    partial_update:
    Update partial data of given .
    """
    queryset = User.objects.all()
    permission_classes = (
        permissions.AllowAnyCreateUpdateIsAdminOrOwner,
        permissions.AllowListIsAdmin,
    )

    def get_serializer_class(self):
        if self.action == 'create':
            if self.request and self.request.user.is_staff:
                return serializers.FullUserCreateSerializer
            return serializers.UserCreateSerializer

        if self.request and self.request.user.is_staff:
            return serializers.FullUserSerializer
        return serializers.UserSerializer
