import pytest
from mixer.backend.django import mixer

from accounts.serializers import UserSerializer


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-04 13:30:55')
class TestUserSerializer:
    @pytest.fixture
    def data(self):
        return {
            'uri': (
                'http://testserver/api/auth/users/'
                '4af5528b-0b75-44d9-aaf4-995f7f0849e3/'
            ),
            'pk': '4af5528b-0b75-44d9-aaf4-995f7f0849e3',
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
            'last_login': None,
            'created_at': '2018-01-04T13:30:55Z',
            'updated_at': '2018-01-04T13:30:55Z',
        }

    def test_excepted_data(self, data, user_model, serializer_context):
        user = mixer.blend(user_model, **data)
        serializer = UserSerializer(instance=user, context=serializer_context)
        assert serializer.data == data

    def test_create(self, data, user_model):
        data['password'] = 'secretPass123'
        serializer = UserSerializer(instance=None, data=data)
        assert serializer.is_valid()

        serializer.create(serializer.validated_data)
        user = user_model.objects.get(email=data['email'])
        assert user.check_password(data['password'])

    def test_update(self, data, user):
        old_pass = 'oldpassword123'
        new_pass = 'newpassword123'
        user.set_password(old_pass)
        user.save()
        data['password'] = new_pass

        serializer = UserSerializer(instance=None, data=data)
        assert serializer.is_valid()

        serializer.update(user, serializer.validated_data)
        user.refresh_from_db()
        assert not user.check_password(new_pass)
