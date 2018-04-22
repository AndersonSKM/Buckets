from core.permissions import AnonCreateUserUpdateSelfOnly, ListUserAdminOnly
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from accounts.serializers import GroupSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (
        AnonCreateUserUpdateSelfOnly,
        ListUserAdminOnly,
    )


class GroupViewSet(ModelViewSet):
    permission_classes = (IsAdminUser,)
    serializer_class = GroupSerializer
    queryset = Group.objects.all()
