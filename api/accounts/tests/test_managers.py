import pytest
from mixer.backend.django import mixer

from accounts.models import User


@pytest.mark.django_db
class TestUserManager:
    @pytest.fixture
    def data(self):
        return {
            'email': 'bruce@we.com',
            'password': '|e_Aub*SF.9F',
            'first_name': 'bruce',
            'last_name': 'wayne',
        }

    def test_create_user(self, data):
        user = User.objects.create_user(**data)

        assert user.email == data['email']
        assert user.first_name == data['first_name']
        assert user.last_name == data['last_name']
        assert user.check_password(data['password'])
        assert not user.is_staff
        assert not user.is_superuser
        assert user.is_active

    def test_create_superuser(self, data):
        user = User.objects.create_superuser(**data)

        assert user.is_staff
        assert user.is_superuser
        assert user.is_active

    def test_get_active_users(self):
        active_user = mixer.blend(User, is_active=True)
        inactive_user = mixer.blend(User, is_active=False)

        results = User.objects.get_active_users()
        assert len(results) == 1
        assert inactive_user not in results
        assert active_user in results

    def test_get_active_or_none(self):
        user = mixer.blend(User, is_active=True)
        assert User.objects.get_active_or_none(email=user.email)

        user = mixer.blend(User, is_active=False)
        assert not User.objects.get_active_or_none(email=user.email)
