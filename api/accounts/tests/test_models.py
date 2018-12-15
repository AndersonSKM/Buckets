import pytest
from mock import patch

from accounts.models import User


class TestUser:
    @pytest.fixture
    def user(self):
        return User(email='test@test.com', first_name='John', last_name='Doe')

    def test_str(self, user):
        assert str(user) == user.email

    def test_get_full_name(self, user):
        assert user.get_full_name() == f'{user.first_name} {user.last_name}'

    def test_get_short_name(self, user):
        assert user.get_short_name() == user.first_name

    @patch('accounts.models.AbstractBaseModel.save')
    def test_save_superuser_set_is_staff_true(self, mock_save, user):
        user.is_staff = False
        user.is_superuser = True
        user.save()

        assert user.is_staff
        assert user.is_superuser
        assert mock_save.called
