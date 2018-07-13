import pytest
from mock import MagicMock

from core.permissions import AllowAnyCreateUpdateIsAdminOrOwner, AllowListIsAdmin


class TestAnonCreateUserUpdateSelfOnly:
    @pytest.fixture
    def permission(self):
        return AllowAnyCreateUpdateIsAdminOrOwner()

    @pytest.mark.parametrize('action, is_authenticated, expected', [
        ('create', False, True),
        ('create', True, True),
        ('list', False, False),
        ('list', True, True),
        ('retrieve', False, False),
        ('retrieve', True, True),
        ('update', False, False),
        ('update', True, True),
        ('partial_update', False, False),
        ('partial_update', True, True),
        ('destroy', False, False),
        ('destroy', True, True),
    ])
    def test_has_permission(self, permission, action, is_authenticated, expected):
        view = MagicMock(action=action)
        user = MagicMock(is_authenticated=is_authenticated)
        request = MagicMock(user=user)
        assert permission.has_permission(request, view) == expected

    @pytest.mark.parametrize('action, user_id, obj_id, is_staff, expected', [
        ('retrieve', 1, 1, False, True),
        ('retrieve', 1, 2, False, False),
        ('retrieve', 1, 1, True, True),
        ('retrieve', 1, 2, True, True),
        ('list', 1, 1, False, False),
        ('list', 1, 2, False, False),
        ('list', 1, 1, True, False),
        ('list', 1, 2, True, False),
        ('update', 1, 1, False, True),
        ('update', 1, 2, False, False),
        ('update', 1, 1, True, True),
        ('update', 1, 2, True, True),
        ('partial_update', 1, 1, False, True),
        ('partial_update', 1, 2, False, False),
        ('partial_update', 1, 1, True, True),
        ('partial_update', 1, 2, True, True),
        ('destroy', 1, 1, False, True),
        ('destroy', 1, 2, False, False),
        ('destroy', 1, 1, True, True),
        ('destroy', 1, 2, True, True),
    ])
    def test_has_object_permission(self, permission, action, user_id, obj_id, is_staff, expected):
        view = MagicMock(action=action)
        user = MagicMock(id=user_id, is_staff=is_staff)
        request = MagicMock(user=user)
        obj = MagicMock(id=obj_id)
        assert permission.has_object_permission(request, view, obj) == expected


class TestListUserAdminOnly:
    @pytest.fixture
    def permission(self):
        return AllowListIsAdmin()

    @pytest.mark.parametrize('action, is_authenticated, is_staff, expected', [
        ('list', False, False, False),
        ('list', True, False, False),
        ('list', True, True, True),
        ('retrieve', False, False, True),
        ('retrieve', True, False, True),
        ('retrieve', True, True, True),
    ])
    def test_has_permission(self, permission, action, is_authenticated, is_staff, expected):
        view = MagicMock(action=action)
        user = MagicMock(is_authenticated=is_authenticated, is_staff=is_staff)
        request = MagicMock(user=user)
        assert permission.has_permission(request, view) == expected
