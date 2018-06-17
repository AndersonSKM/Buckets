from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from accounts import serializers
from core import permissions

User = get_user_model()


class UserViewSet(ModelViewSet):
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
