import pytest
from mixer.backend.django import mixer
from mock import Mock
from testfixtures import should_raise

from accounts.models import User


class TestUser:
    @pytest.fixture
    def user(self):
        user = User(email='test@test.com', first_name='John', last_name='Doe')
        user.default_save = user.save
        user.save = Mock()
        user.full_clean = Mock()
        return user

    def test_str(self, user):
        assert str(user) == user.email

    def test_get_full_name(self, user):
        assert user.get_full_name() == f'{user.first_name} {user.last_name}'

    def test_get_short_name(self, user):
        assert user.get_short_name() == user.first_name

    @pytest.mark.django_db
    def test_save_superuser_set_is_staff_true(self, user):
        user.is_staff = False
        user.is_superuser = True
        user.default_save()

        assert user.is_staff
        assert user.is_superuser

    def test_activate_inactive_user(self, user):
        user.is_active = False
        user.activate()

        assert user.is_active
        assert user.save.called

    def test_activate_active_user(self, user):
        user.is_active = True
        user.activate()

        assert user.is_active
        assert not user.save.called


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
        assert User.objects.get_or_none(email=data['email'])
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

    def test_active(self):
        active_user = mixer.blend(User, is_active=True)
        inactive_user = mixer.blend(User, is_active=False)
        results = User.objects.active()

        assert len(results) == 1
        assert inactive_user not in results
        assert active_user in results

    def test_get_active_or_none(self):
        user = mixer.blend(User, is_active=True)
        assert User.objects.get_active_or_none(email=user.email)

        user = mixer.blend(User, is_active=False)
        assert not User.objects.get_active_or_none(email=user.email)
