import pytest
from mock import patch

from accounts import serializers


class TestCreateUserSerializers:
    @pytest.fixture
    def data(self):
        return {
            'email': 'vader@deathstar.com',
            'password': 'secretPass123',
            'first_name': 'Anakin',
            'last_name': 'Skywalker',
        }

    @patch('accounts.serializers.validate_password')
    @patch('accounts.serializers.User')
    def test_create(self, mock_user, mock_validate_password, data, anon_user):
        mock_user.objects.create_user.return_value = anon_user
        serializer = serializers.UserCreateSerializer(data=data)
        serializer.create(data)

        mock_user.objects.create_user.assert_called_once_with(
            'vader@deathstar.com',
            'secretPass123',
            False,
            first_name='Anakin',
            last_name='Skywalker',
        )
        mock_validate_password.assert_called_once_with('secretPass123', anon_user)
