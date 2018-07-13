import pytest
from mock import Mock

from accounts.serializers import (
    FullUserCreateSerializer,
    FullUserSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from accounts.views import UserViewSet


class TestUsersApiViewSet:
    @pytest.fixture
    def view(self):
        view = UserViewSet()
        view.request = Mock()
        return view

    @pytest.mark.parametrize('is_staff, action, expected', [
        (False, 'create', UserCreateSerializer),
        (True, 'create', FullUserCreateSerializer),
        (False, 'retrieve', UserSerializer),
        (True, 'retrieve', FullUserSerializer),
        (False, 'list', UserSerializer),
        (True, 'list', FullUserSerializer),
        (False, 'update', UserSerializer),
        (True, 'update', FullUserSerializer),
        (False, 'partial_update', UserSerializer),
        (True, 'partial_update', FullUserSerializer),
    ])
    def test_get_serializer_class(self, view, is_staff, action, expected):
        view.request.user.is_staff = is_staff
        view.action = action
        assert view.get_serializer_class() == expected
