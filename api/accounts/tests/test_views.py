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

    def test_get_serializer_class_create_standard_user(self, view):
        view.request.user.is_staff = False
        view.action = 'create'
        assert view.get_serializer_class() == UserCreateSerializer

    def test_get_serializer_class_create_staff_user(self, view):
        view.request.user.is_staff = True
        view.action = 'create'
        assert view.get_serializer_class() == FullUserCreateSerializer

    def test_get_serializer_class_standard_user(self, view):
        view.request.user.is_staff = False
        view.action = 'retrieve'
        assert view.get_serializer_class() == UserSerializer

    def test_get_serializer_class_staff_user(self, view):
        view.request.user.is_staff = True
        view.action = 'retrieve'
        assert view.get_serializer_class() == FullUserSerializer
