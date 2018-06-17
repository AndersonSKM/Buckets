import pytest
from django.urls import reverse
from mixer.backend.django import mixer
from mock import Mock
from rest_framework import status

from accounts.serializers import (
    FullUserCreateSerializer,
    FullUserSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from accounts.views import UserViewSet


class TestUsersApiViewSet:
    @pytest.fixture
    def view(self):
        view = UserViewSet()
        view.request = Mock()
        return view

    def test_get_serializer_class_create_standard_user(self, view):
        view.request.user.is_staff = False
        view.action = 'create'
        assert view.get_serializer_class() == UserCreateSerializer

    def test_get_serializer_class_create_staff_user(self, view):
        view.request.user.is_staff = True
        view.action = 'create'
        assert view.get_serializer_class() == FullUserCreateSerializer

    def test_get_serializer_class_standard_user(self, view):
        view.request.user.is_staff = False
        view.action = 'retrieve'
        assert view.get_serializer_class() == UserSerializer

    def test_get_serializer_class_staff_user(self, view):
        view.request.user.is_staff = True
        view.action = 'retrieve'
        assert view.get_serializer_class() == FullUserSerializer


@pytest.mark.django_db
class TestUsersApiViewSetIntegration:
    @pytest.fixture
    def data(self):
        return {
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'password': 'secretPa$$123',
            'password_confirm': 'secretPa$$123',
            'is_superuser': False,
            'is_active': True,
        }

    def test_create_anon_user(self, api_client, user_model, data):
        url = reverse('auth:users-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        user = user_model.objects.get(email=data['email'])
        assert not user.is_staff
        assert not user.is_active

    def test_admin_create_staff_user(self, api_adm_client, user_model, data):
        data['is_staff'] = True
        url = reverse('auth:users-list')
        response = api_adm_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

        user = user_model.objects.get(email=data['email'])
        assert user.is_staff
        assert not user.is_active

    def test_list_anon_user(self, api_client):
        url = reverse('auth:users-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_auth_normal_user(self, api_auth_client):
        url = reverse('auth:users-list')
        response = api_auth_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_auth_adm_user(self, api_adm_client):
        url = reverse('auth:users-list')
        response = api_adm_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_update_other_record(self, api_auth_client, user_model):
        user = mixer.blend(user_model, first_name='Bruce')

        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.patch(url, {'first_name': 'Batman'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_self_record(self, api_auth_client, user_model, user):
        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.patch(url, {'first_name': 'Batman'})
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.first_name == 'Batman'

    def test_update_adm_user(self, api_adm_client, user_model):
        user = mixer.blend(user_model, first_name='Bruce')

        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_adm_client.patch(url, {'first_name': 'Batman'})
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.first_name == 'Batman'

    def test_adm_user_update_is_staff(self, api_adm_client, user_model):
        user = mixer.blend(user_model, is_staff=False)

        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_adm_client.patch(url, {'is_staff': True})
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.is_staff

    def test_standard_user_update_is_staff(self, api_auth_client, user):
        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.patch(url, {'is_staff': True})
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert not user.is_staff

    def test_block_update_password(self, api_adm_client, user):
        data = {'password': 'HackPasswd'}

        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_adm_client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert not user.check_password(data['password'])

    def test_delete_self_record(self, api_auth_client, user_model, user):
        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not user_model.objects.filter(pk=user.pk).exists()

    def test_delete_other_record(self, api_auth_client, user_model):
        user = mixer.blend(user_model)

        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_adm_user(self, api_adm_client, user_model):
        user = mixer.blend(user_model)

        url = reverse('auth:users-detail', kwargs={'pk': user.pk})
        response = api_adm_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT
