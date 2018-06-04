import pytest
from mock import MagicMock

from core.permissions import AnonCreateUserUpdateSelfOnly, ListUserAdminOnly


class TestAnonCreateUserUpdateSelfOnly:
    @pytest.fixture
    def permission(self):
        return AnonCreateUserUpdateSelfOnly()

    def test_has_permission_create(self, permission):
        view = MagicMock(action='create')
        request = MagicMock(user=None)
        assert permission.has_permission(request, view)

    def test_has_object_permission_retrieve(self, permission):
        self._check_obj_permissions(permission, 'retrieve')

    def test_has_object_permission_update(self, permission):
        self._check_obj_permissions(permission, 'update')

    def test_has_object_permission_partial_update(self, permission):
        self._check_obj_permissions(permission, 'partial_update')

    def test_has_object_permission_delete(self, permission):
        self._check_obj_permissions(permission, 'destroy')

    def _check_obj_permissions(self, permission, action):
        view = MagicMock(action=action)
        user = MagicMock(is_authenticated=True, id=1, is_staff=False)
        request = MagicMock(user=user)
        obj = MagicMock(id=2)
        assert not permission.has_object_permission(request, view, obj)

        user = MagicMock(is_authenticated=True, id=1, is_staff=True)
        request = MagicMock(user=user)
        obj = MagicMock(id=3)
        assert permission.has_object_permission(request, view, obj)

        user = MagicMock(is_authenticated=True, id=1, is_staff=False)
        request = MagicMock(user=user)
        obj = MagicMock(id=user.id)
        assert permission.has_object_permission(request, view, obj)


class TestListUserAdminOnly:
    @pytest.fixture
    def permission(self):
        return ListUserAdminOnly()

    def test_has_permission(self, permission):
        view = MagicMock(action='list')
        request = MagicMock(user=None)
        assert not permission.has_permission(request, view)

        user = MagicMock(is_staff=False)
        request = MagicMock(user=user)
        assert not permission.has_permission(request, view)

        user = MagicMock(is_staff=True)
        request = MagicMock(user=user)
        assert permission.has_permission(request, view)

        view = MagicMock(action='retrieve')
        request = MagicMock(user=None)
        assert permission.has_permission(request, view)
