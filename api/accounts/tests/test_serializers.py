import mock
import pytest
from mixer.backend.django import mixer
from rest_framework.exceptions import ValidationError
from testfixtures import should_raise

from accounts import serializers


@pytest.mark.django_db
class TestCreateUserSerializers:
    @pytest.fixture
    def user_data(self):
        return {
            'email': 'vader@deathstar.com',
            'password': 'secretPass123',
            'password_confirm': 'secretPass123',
            'first_name': 'Anakin',
            'last_name': 'Skywalker',
        }

    @mock.patch('accounts.serializers.User')
    def test_create_normal_serializer(self, user_model, user_data):
        serializer = serializers.UserCreateSerializer(data=user_data)
        assert serializer.is_valid()
        serializer.create(user_data.copy())

        user_model.objects.create_user.assert_called_once_with(
            user_data['email'],
            user_data['password'],
            False,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )

    @mock.patch('accounts.serializers.User')
    def test_create_full_serializer(self, user_model, user_data):
        user_data['is_staff'] = True
        serializer = serializers.FullUserCreateSerializer(data=user_data)
        assert serializer.is_valid()
        serializer.create(user_data.copy())

        user_model.objects.create_user.assert_called_once_with(
            user_data['email'],
            user_data['password'],
            True,
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
        )

    @should_raise(ValidationError("Passwords don't match."))
    def test_validate_password_confirm_invalid(self, user_data):
        user_data['password_confirm'] = 'abracadabra'
        serializer = serializers.FullUserCreateSerializer(data=user_data)

        assert not serializer.is_valid()
        serializer.validate(user_data)


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-04 13:30:55')
class TestUserSerializer:
    @pytest.fixture
    def user_data(self):
        return {
            'uri': 'http://testserver/api/auth/users/4af5528b-0b75-44d9-aaf4-995f7f0849e3/',
            'pk': '4af5528b-0b75-44d9-aaf4-995f7f0849e3',
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'is_staff': False,
            'is_superuser': False,
            'is_active': False,
            'last_login': None,
            'created_at': '2018-01-04T13:30:55Z',
            'updated_at': '2018-01-04T13:30:55Z',
        }

    def test_expected_data(self, user_model, user_data, serializer_context):
        user = mixer.blend(user_model, **user_data)
        serializer = serializers.FullUserSerializer(
            instance=user,
            context=serializer_context
        )
        assert serializer.data == user_data
