import pytest
from mock import MagicMock

from core.permissions import AllowAnyCreateUpdateIsOwner


class TestAnonCreateUserUpdateSelfOnly:
    @pytest.fixture
    def permission(self):
        return AllowAnyCreateUpdateIsOwner()

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

    @pytest.mark.parametrize('action, user_id, obj_id, expected', [
        ('list', 1, 1, False),
        ('list', 1, 2, False),
        ('retrieve', 1, 1, True),
        ('retrieve', 1, 2, False),
        ('update', 1, 1, True),
        ('update', 1, 2, False),
        ('partial_update', 1, 1, True),
        ('partial_update', 1, 2, False),
        ('destroy', 1, 1, True),
        ('destroy', 1, 2, False),
    ])
    def test_has_object_permission(self, permission, action, user_id, obj_id, expected):
        view = MagicMock(action=action)
        user = MagicMock(id=user_id)
        request = MagicMock(user=user)
        obj = MagicMock(id=obj_id)
        assert permission.has_object_permission(request, view, obj) == expected
