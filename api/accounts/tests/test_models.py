import pytest
from testfixtures import should_raise

from accounts.models import User


@pytest.mark.django_db
class TestUser:
    def test_str(self, user):
        assert str(user) == user.email

    def test_get_full_name(self, user):
        assert user.get_full_name() == f'{user.first_name} {user.last_name}'

    def test_get_short_name(self, user):
        assert user.get_short_name() == user.first_name

    def test_save_superuser_set_is_staff_true(self, user):
        user.is_superuser = True
        user.save()
        assert user.is_staff


@pytest.mark.django_db
class TestUserManager:
    @pytest.fixture
    def data(self):
        return {
            'email': 'bruce@we.com',
            'password': 'batman',
            'first_name': 'bruce',
            'last_name': 'wayne',
        }

    def test_create_user(self, data):
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        assert User.objects.filter(email=data['email']).exists()
        assert user.email == data['email']
        assert user.first_name == data['first_name']
        assert user.last_name == data['last_name']
        assert user.check_password(data['password'])
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_active

    def test_create_superuser(self, data):
        user = User.objects.create_superuser(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active

    @should_raise(ValueError("Users must have an email address"))
    def test_invalid_email(self):
        User.objects.create_user(email=None, password=None)
