import pytest
from core.utils.tests import raises

from accounts.models import User


@pytest.mark.django_db
class TestUser:
    def test_str(self, user):
        assert str(user) == user.email

    def test_get_full_name(self, user):
        assert user.get_full_name() == \
            "%s %s" % (user.first_name, user.last_name)

    def test_get_short_name(self, user):
        assert user.get_short_name() == user.first_name

    def test_is_admin(self):
        user = User(is_staff=True)
        assert user.is_admin

        user = User(is_superuser=True)
        assert user.is_admin

        user = User()
        assert not user.is_admin


@pytest.mark.django_db
class TestUserManager:
    data = {
        'email': 'bruce@we.com',
        'password': 'batman',
        'first_name': 'bruce',
        'last_name': 'wayne',
    }

    def test_create_user(self):
        user = User.objects.create_user(
            email=self.data['email'],
            password=self.data['password'],
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
        )
        assert User.objects.filter(email=self.data['email']).exists()
        assert user.email == self.data['email']
        assert user.first_name == self.data['first_name']
        assert user.last_name == self.data['last_name']
        assert user.check_password(self.data['password'])
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_active

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email=self.data['email'],
            password=self.data['password'],
            first_name=self.data['first_name'],
            last_name=self.data['last_name'],
        )
        assert user.is_staff
        assert user.is_superuser
        assert user.is_active

    @raises(ValueError, "Users must have an email address")
    def test_invalid_email(self):
        User.objects.create_user(email=None, password=None)
