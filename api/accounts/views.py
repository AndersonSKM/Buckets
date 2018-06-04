from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import UserSerializer
from core.permissions import AnonCreateUserUpdateSelfOnly, ListUserAdminOnly


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (
        AnonCreateUserUpdateSelfOnly,
        ListUserAdminOnly,
    )
