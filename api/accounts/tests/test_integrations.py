"""
import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from mixer.backend.django import mixer
from mock import patch
from rest_framework import status

from accounts.models import User
from accounts.serializers import UserSerializer
from accounts.utils import encode_user_uuid, user_activation_token


@pytest.fixture
def user_data():
    return {
        'url': 'http://testserver/api/users/4af5528b-0b75-44d9-aaf4-995f7f0849e3/',
        'pk': '4af5528b-0b75-44d9-aaf4-995f7f0849e3',
        'email': 'bruce@we.com',
        'first_name': 'Bruce',
        'last_name': 'Wayne',
        'created_at': '2018-01-04T13:30:55Z',
        'updated_at': '2018-01-04T13:30:55Z',
    }


@pytest.mark.django_db
class TestUsersApiCreateIntegration:
    @pytest.fixture
    def data(self):
        return {
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'password': 'secretPa$$123',
            'password_confirm': 'secretPa$$123',
        }

    @pytest.fixture()
    def url(self):
        return reverse('accounts:users-list')

    def test_anonymous_user(self, anonymous_client, url, data, mailoutbox):
        response = anonymous_client.post(path=url, data=data)
        user = User.objects.get_by_natural_key(data['email'])

        assert response.status_code == status.HTTP_201_CREATED
        assert not user.is_staff
        assert not user.is_active
        assert len(mailoutbox) == 1

    @patch('accounts.managers.UserManager.send_activation_email')
    def test_send_email_fail(self, send_email, anonymous_client, url, data):
        send_email.side_effect = Exception("Error to send email")
        response = anonymous_client.post(path=url, data=data)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['detail'] == "Error to send email"
        assert not User.objects.get_or_none(email=data['email'])

    def test_wrong_password_confirm(self, anonymous_client, url, data):
        data['password_confirm'] = 'Wrongpasswordconfirm'
        response = anonymous_client.post(path=url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Passwords don't match."]
        assert not User.objects.get_or_none(email=data['email'])

    def test_weak_password(self, anonymous_client, url, data):
        data['password'] = 'bruce'
        data['password_confirm'] = data['password']
        response = anonymous_client.post(path=url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) > 0
        assert not User.objects.get_or_none(email=data['email'])


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-04 13:30:55')
class TestUsersApiRetrieveIntegration:
    @pytest.fixture()
    def url(self):
        return reverse(
            'accounts:users-detail',
            kwargs={'pk': '4af5528b-0b75-44d9-aaf4-995f7f0849e3'}
        )

    @pytest.fixture()
    def data(self):
        return {
            'url': 'http://testserver/api/users/4af5528b-0b75-44d9-aaf4-995f7f0849e3/',
            'pk': '4af5528b-0b75-44d9-aaf4-995f7f0849e3',
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'is_active': True,
            'created_at': '2018-01-04T13:30:55Z',
            'updated_at': '2018-01-04T13:30:55Z',
        }

    def test_retrieve_self_instance(self, anonymous_client, url, data, jwt):
        user = mixer.blend(User, **data)

        token = jwt(user)
        anonymous_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == data

    def test_retrieve_other_user(self, client, url, data):
        mixer.blend(User, **data)
        response = client.get(path=url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user(self, anonymous_client, url):
        response = anonymous_client.get(path=url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUsersApiUpdateIntegration:
    @pytest.fixture()
    def url(self, user):
        return reverse('accounts:users-detail', kwargs={'pk': user.pk})

    def test_update_other_record(self, client):
        user = mixer.blend(User, first_name='Bruce')
        url = reverse('accounts:users-detail', kwargs={'pk': user.pk})
        response = client.patch(path=url, data={'first_name': 'Batman'})

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_self_record(self, client, url, user):
        response = client.patch(path=url, data={'first_name': 'Batman'})
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.first_name == 'Batman'

    def test_block_update_is_staff_and_is_superuser(self, client, url, user):
        response = client.patch(path=url, data={'is_staff': True, 'is_superuser': True})
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert not user.is_staff
        assert not user.is_superuser

    def test_block_update_password(self, client, url, user):
        data = {'password': 'HackPasswd'}
        response = client.patch(path=url, data=data, pk=user.pk)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert not user.check_password(data['password'])

    def test_anonymous_user(self, anonymous_client, url, user):
        response = anonymous_client.patch(path=url, data={'first_name': 'Batman'})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUsersApiDeleteIntegration:
    @pytest.fixture()
    def url(self, user):
        return reverse('accounts:users-detail', kwargs={'pk': user.pk})

    def test_delete_self_record(self, client, url, user):
        response = client.delete(path=url, follow=True)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.get_or_none(pk=user.pk)

    def test_delete_other_record(self, client):
        user = mixer.blend(User)
        url = reverse('accounts:users-detail', kwargs={'pk': user.pk})
        response = client.delete(path=url, follow=True)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_anonymous_user(self, anonymous_client, url):
        response = anonymous_client.delete(path=url, follow=True)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestUsersApiActivateIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:users-activate')

    def test_successful(self, anonymous_client, url):
        user = mixer.blend(User, is_active=False)
        data = {
            'uuidb64': encode_user_uuid(user.pk),
            'token': user_activation_token.make_token(user),
        }
        response = anonymous_client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.is_active

    def test_invalid_uuid(self, anonymous_client, url):
        data = {
            'uuidb64': 'OTZmMjg0ZjUtOWVlNC00ZmZmLTk2OGQtOWM5MzZjYzQ4ZWRl',
            'token': '4y7-d387414eda804361f681',
        }
        response = anonymous_client.post(path=url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Invalid user id or user doesn't exist."]

    def test_invalid_token(self, anonymous_client, url, user):
        data = {
            'uuidb64': encode_user_uuid(user.pk),
            'token': '4y7-d387414eda804361f681',
        }
        response = anonymous_client.post(path=url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Invalid token for given user."]


@pytest.mark.django_db
class TestUsersApiPasswordForgotIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:users-password-forgot')

    def test_successful(self, anonymous_client, url, user, mailoutbox):
        response = anonymous_client.post(path=url, data={'email': user.email})

        assert response.status_code == status.HTTP_200_OK
        assert len(mailoutbox) == 1

    def test_invalid_email(self, anonymous_client, url, user, mailoutbox):
        response = anonymous_client.post(path=url, data={'email': 'fake@fake.com'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Invalid email or user doesn't exist."]
        assert len(mailoutbox) == 0

    @patch('accounts.managers.UserManager.send_password_reset_email')
    def test_send_email_fail(self, send_email, client, url, user):
        send_email.side_effect = Exception("Error to send email")
        response = client.post(path=url, data={'email': user.email})

        assert send_email.called
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['detail'] == "Error to send email"


@pytest.mark.django_db
class TestUsersApiPasswordResetIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:users-password-reset')

    @pytest.fixture
    def data(self, user):
        return {
            'uuidb64': encode_user_uuid(user.pk),
            'token': default_token_generator.make_token(user),
            'password': 'New$ecretPass%',
            'password_confirm': 'New$ecretPass%',
        }

    def test_successful(self, anonymous_client, url, data, user):
        response = anonymous_client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(data['password'])

    def test_weak_password(self, anonymous_client, url, data, user):
        data['password'] = 'qwerty'
        data['password_confirm'] = 'qwerty'
        response = anonymous_client.post(path=url, data=data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) > 1

    def test_invalid_passowrd_confirm(self, anonymous_client, url, data, user):
        data['password_confirm'] = 'invalid'
        response = anonymous_client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Passwords don't match."]
        assert not user.check_password(data['password'])


@pytest.mark.django_db
class TestUsersApiChangePassowordIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:users-change-password')

    @pytest.fixture
    def data(self, user):
        fields = {
            'current_password': 'MyOldPa$$w0rd',
            'password': 'New$ecretPass%',
            'password_confirm': 'New$ecretPass%',
        }
        user.set_password(fields['current_password'])
        user.save()
        return fields

    def test_successful(self, client, url, data, user):
        response = client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.check_password(data['password'])

    def test_anonymous_user(self, anonymous_client, url, data):
        response = anonymous_client.post(path=url, data=data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_wrong_current_password(self, client, url, data, user):
        data['current_password'] = 'Dummy'
        response = client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Invalid current password."]

    def test_weak_password(self, client, url, data, user):
        data['password'] = 'qwerty'
        data['password_confirm'] = 'qwerty'
        response = client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) > 1
        assert not user.check_password(data['password'])

    def test_invalid_passowrd_confirm(self, client, url, data, user):
        data['password_confirm'] = 'invalid'
        response = client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Passwords don't match."]
        assert not user.check_password(data['password'])


@pytest.mark.django_db
class TestTokensApiObtainTokenIntegration:
    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            email='superman@us.com',
            password='secretPa$$123',
            confirm='secretPa$$123'
        )

    @pytest.fixture
    def url(self):
        return reverse('accounts:obtain-token')

    def test_obtain_token_invalid_credentials(self, url, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'email': 'fake@fake.com',
            'password': 'aslfoakf3'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == [
            'Unable to log in with provided credentials.'
        ]

    def test_obtain_token_inactive_user(self, url, user, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'email': 'superman@us.com',
            'password': 'secretPa$$123'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["User account is disabled."]

    @pytest.mark.freeze_time('2018-01-04 13:30:55')
    def test_obtain_token_active_user(self, url, user, anonymous_client, jwt, serializer_context):
        User.objects.activate(user=user)
        response = anonymous_client.post(path=url, data={
            'email': 'superman@us.com',
            'password': 'secretPa$$123'
        })
        expected_data = UserSerializer(user, context=serializer_context).data

        assert response.status_code == status.HTTP_200_OK
        assert response.data['token'] == jwt(user)
        assert response.data['user'] == expected_data


@pytest.mark.django_db
class TestTokensApiRefreshTokenIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:refresh-token')

    def test_refresh_token_invalid_data(self, jwt, user, url, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'token': 'asdaosd1201k1do312mdkmm2im3rk213',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ['Error decoding signature.']

    def test_refresh_token_valid_data(self, jwt, url, user, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'token': jwt(user)
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['token'] == jwt(user)
"""
