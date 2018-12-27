import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from djoser.utils import encode_uid
from mixer.backend.django import mixer
from rest_framework import status

from accounts.models import User


@pytest.fixture
def user_data():
    return {
        'first_name': 'Bruce',
        'last_name': 'Wayne',
        'id': '4af5528b-0b75-44d9-aaf4-995f7f0849e3',
        'email': 'bruce@we.com',
        'created_at': '2018-01-04T13:30:55Z',
        'updated_at': '2018-01-04T13:30:55Z',
    }


@pytest.mark.django_db
class TestUsersApiCreateIntegration:
    @pytest.fixture
    def input_data(self):
        return {
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'password': 'secretPa$$123',
        }

    @pytest.fixture()
    def url(self):
        return reverse('accounts:user-create')

    def test_anonymous_user(self, anonymous_client, url, input_data, mailoutbox):
        response = anonymous_client.post(path=url, data=input_data)
        user = User.objects.get_by_natural_key(input_data['email'])

        assert response.status_code == status.HTTP_201_CREATED
        assert len(mailoutbox) == 1
        assert not user.is_staff
        assert not user.is_active

    def test_weak_password(self, anonymous_client, url, input_data):
        input_data['password'] = 'bruce'
        response = anonymous_client.post(path=url, data=input_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['password']) > 0
        assert not User.objects.get_or_none(email=input_data['email'])


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-04T13:30:55')
class TestUsersApiRetrieveIntegration:
    @pytest.fixture()
    def url(self):
        return reverse('accounts:user')

    def test_retrieve_self_record(self, anonymous_client, url, user_data, jwt):
        user = mixer.blend(User, is_active=True, **user_data)

        token = jwt(user)
        anonymous_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == user_data


@pytest.mark.django_db
class TestUsersApiUpdateIntegration:
    @pytest.fixture()
    def url(self):
        return reverse('accounts:user')

    def test_update_self_record(self, client, url, user):
        response = client.patch(path=url, data={'first_name': 'Austin Powers'})
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert user.first_name == 'Austin Powers'

    def test_block_update_is_staff_and_is_superuser(self, client, url, user):
        response = client.patch(path=url, data={'is_staff': True, 'is_superuser': True})
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert not user.is_staff
        assert not user.is_superuser

    def test_block_update_password(self, client, url, user):
        input_data = {'password': 'HackPasswd'}
        response = client.patch(path=url, data=input_data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert not user.check_password(input_data['password'])


@pytest.mark.django_db
class TestUsersApiDeleteIntegration:
    @pytest.fixture()
    def url(self):
        return reverse('accounts:user-me')

    def test_successfull_delete(self, user, client, url):
        response = client.delete(path=url, data={'current_password': 'user'}, follow=True)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.get_or_none(pk=user.pk)

    def test_delete_fail_with_wrong_password(self, user, client, url):
        response = client.delete(path=url, data={'current_password': 'qwert'}, follow=True)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['current_password'] == ['Invalid password.',]
        assert User.objects.get_or_none(pk=user.pk)


@pytest.mark.django_db
class TestUsersApiActivateIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:user-activate')

    def test_successful_activation(self, anonymous_client, url):
        user = mixer.blend(User, is_active=False)
        data = {
            'uid': encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
        }
        response = anonymous_client.post(path=url, data=data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert user.is_active


@pytest.mark.django_db
class TestUsersApiPasswordResetIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:password_reset')

    def test_successful(self, anonymous_client, url, user, mailoutbox):
        response = anonymous_client.post(path=url, data={'email': user.email})

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert len(mailoutbox) == 1

    def test_invalid_email(self, anonymous_client, url, user, mailoutbox):
        response = anonymous_client.post(path=url, data={'email': 'fake@fake.com'})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(mailoutbox) == 0


@pytest.mark.django_db
class TestUsersApiPasswordResetConfirmIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:password_reset_confirm')

    @pytest.fixture
    def input_data(self, user):
        return {
            'uid': encode_uid(user.pk),
            'token': default_token_generator.make_token(user),
            'new_password': 'New$ecretPass%',
            're_new_password': 'New$ecretPass%',
        }

    def test_successful(self, anonymous_client, url, input_data, user):
        response = anonymous_client.post(path=url, data=input_data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert user.check_password(input_data['new_password'])

    def test_weak_password(self, anonymous_client, url, input_data, user):
        input_data['new_password'] = 'qwerty'
        input_data['re_new_password'] = 'qwerty'
        response = anonymous_client.post(path=url, data=input_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['new_password']) > 1

    def test_invalid_passowrd_confirm(self, anonymous_client, url, input_data, user):
        input_data['re_new_password'] = 'invalid'
        response = anonymous_client.post(path=url, data=input_data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) == 1


@pytest.mark.django_db
class TestUsersApiChangePassowordIntegration:
    @pytest.fixture
    def url(self):
        return reverse('accounts:set_password')

    @pytest.fixture
    def input_data(self, user):
        fields = {
            'current_password': 'MyOldPa$$w0rd',
            'new_password': 'New$ecretPass%',
            're_new_password': 'New$ecretPass%',
        }
        user.set_password(fields['current_password'])
        user.save()
        return fields

    def test_successful(self, client, url, input_data, user):
        response = client.post(path=url, data=input_data)
        user.refresh_from_db()

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert user.check_password(input_data['new_password'])

    def test_wrong_current_password(self, client, url, input_data, user):
        input_data['current_password'] = 'Dummy'
        response = client.post(path=url, data=input_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['current_password']) == 1

    def test_weak_password(self, client, url, input_data, user):
        input_data['new_password'] = 'qwerty'
        input_data['re_new_password'] = 'qwerty'
        response = client.post(path=url, data=input_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['new_password']) > 1

    def test_invalid_passowrd_confirm(self, client, url, input_data, user):
        input_data['re_new_password'] = 'invalid'
        response = client.post(path=url, data=input_data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) == 1


@pytest.mark.django_db
class TestTokensApiObtainTokenIntegration:
    @pytest.fixture
    def url(self):
        return reverse('auth:jwt-create')

    def test_obtain_token_sucessfull(self, url, user, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'email': user.email,
            'password': 'user'
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['token']

    def test_obtain_token_invalid_credentials(self, url, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'email': 'fake@fake.com',
            'password': 'aslfoakf3'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) == 1

    def test_obtain_token_inactive_user(self, url, inactive_user, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'email': inactive_user.email,
            'password': 'inactive'
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) == 1


@pytest.mark.django_db
class TestTokensApiRefreshTokenIntegration:
    @pytest.fixture
    def url(self):
        return reverse('auth:jwt-refresh')

    def test_refresh_token_invalid_data(self, jwt, user, url, anonymous_client):
        response = anonymous_client.post(path=url, data={
            'token': 'asdaosd1201k1do312mdkmm2im3rk213',
        })

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert len(response.data['non_field_errors']) == 1

    def test_refresh_token_valid_data(self, jwt, url, user, anonymous_client):
        token = jwt(user)
        response = anonymous_client.post(path=url, data={
            'token': token
        })

        assert response.status_code == status.HTTP_200_OK
        assert response.data['token']
