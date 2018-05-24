from mock import MagicMock

from core.permissions import AnonCreateUserUpdateSelfOnly, ListUserAdminOnly


class TestAnonCreateUserUpdateSelfOnly:
    perm = AnonCreateUserUpdateSelfOnly()

    def test_has_permission_create(self):
        view = MagicMock(action='create')
        request = MagicMock(user=None)
        assert self.perm.has_permission(request, view)

    def test_has_object_permission_retrieve(self):
        view = MagicMock(action='retrieve')
        self._check_obj_permissions(view)

    def test_has_object_permission_update(self):
        view = MagicMock(action='update')
        self._check_obj_permissions(view)

    def test_has_object_permission_partial_update(self):
        view = MagicMock(action='partial_update')
        self._check_obj_permissions(view)

    def test_has_object_permission_delete(self):
        view = MagicMock(action='destroy')
        self._check_obj_permissions(view)

    def _check_obj_permissions(self, view):
        user = MagicMock(is_authenticated=True, id=1, is_admin=False)
        request = MagicMock(user=user)
        obj = MagicMock(id=2)
        assert not self.perm.has_object_permission(request, view, obj)

        user = MagicMock(is_authenticated=True, id=1, is_admin=True)
        request = MagicMock(user=user)
        obj = MagicMock(id=3)
        assert self.perm.has_object_permission(request, view, obj)

        user = MagicMock(is_authenticated=True, id=1, is_admin=False)
        request = MagicMock(user=user)
        obj = MagicMock(id=user.id)
        assert self.perm.has_object_permission(request, view, obj)


class TestListUserAdminOnly:
    perm = ListUserAdminOnly()

    def test_has_permission(self):
        view = MagicMock(action='list')
        request = MagicMock(user=None)
        assert not self.perm.has_permission(request, view)

        user = MagicMock(is_admin=False)
        request = MagicMock(user=user)
        assert not self.perm.has_permission(request, view)

        user = MagicMock(is_admin=True)
        request = MagicMock(user=user)
        assert self.perm.has_permission(request, view)

        view = MagicMock(action='retrieve')
        request = MagicMock(user=None)
        assert self.perm.has_permission(request, view)
