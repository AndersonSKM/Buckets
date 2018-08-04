import pytest
from mock import Mock

from accounts.serializers import (
    UserActivateSerializer,
    UserChangePasswordSerializer,
    UserCreateSerializer,
    UserPasswordForgotSerializer,
    UserPasswordResetSerializer,
    UserSerializer,
)
from accounts.views import UserViewSet


class TestUsersApiViewSet:
    @pytest.fixture
    def view(self):
        view = UserViewSet()
        view.request = Mock()
        return view

    @pytest.mark.parametrize('action, expected', [
        ('create', UserCreateSerializer),
        ('retrieve', UserSerializer),
        ('list', UserSerializer),
        ('update', UserSerializer),
        ('partial_update', UserSerializer),
        ('activate', UserActivateSerializer),
        ('password_forgot', UserPasswordForgotSerializer),
        ('password_reset', UserPasswordResetSerializer),
        ('change_password', UserChangePasswordSerializer),
    ])
    def test_get_serializer_class(self, view, action, expected):
        view.action = action
        assert view.get_serializer_class() == expected
