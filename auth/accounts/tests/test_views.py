import pytest
from django.contrib.auth.models import Group
from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status


@pytest.mark.django_db
class TestUsersApiViewSet:
    def test_create_anon_user(self, api_client, user_model):
        data = {
            'email': 'bruce@we.com',
            'first_name': 'Bruce',
            'last_name': 'Wayne',
            'password': 'secretPa$$123',
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
        }

        url = reverse('api:users-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert user_model.objects.get(email=data['email'])

    def test_list_anon_user(self, api_client):
        url = reverse('api:users-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_auth_normal_user(self, api_auth_client, user):
        url = reverse('api:users-list')
        response = api_auth_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_list_auth_adm_user(self, api_adm_client):
        url = reverse('api:users-list')
        response = api_adm_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1

    def test_update_other_record(self, api_auth_client, user_model):
        user = mixer.blend(user_model, first_name='Bruce')

        url = reverse('api:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.patch(url, {'first_name': 'Batman'})
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_update_self_record(self, api_auth_client, user_model, user):
        url = reverse('api:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.patch(url, {'first_name': 'Batman'})
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.first_name == 'Batman'

    def test_update_adm_user(self, api_adm_client, user_model):
        user = mixer.blend(user_model, first_name='Bruce')

        url = reverse('api:users-detail', kwargs={'pk': user.pk})
        response = api_adm_client.patch(url, {'first_name': 'Batman'})
        assert response.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.first_name == 'Batman'

    def test_delete_self_record(self, api_auth_client, user_model, user):
        url = reverse('api:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not user_model.objects.filter(pk=user.pk).exists()

    def test_delete_other_record(self, api_auth_client, user_model):
        user = mixer.blend(user_model)

        url = reverse('api:users-detail', kwargs={'pk': user.pk})
        response = api_auth_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_adm_user(self, api_adm_client, user_model):
        user = mixer.blend(user_model)

        url = reverse('api:users-detail', kwargs={'pk': user.pk})
        response = api_adm_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestGroupApiViewSet:
    def test_create(self, api_adm_client):
        url = reverse('api:groups-list')
        response = api_adm_client.post(url, {'name': 'Awesome Users'})
        assert response.status_code == status.HTTP_201_CREATED
        assert Group.objects.filter(name='Awesome Users').exists()

    def test_read(self, api_adm_client):
        groups = mixer.cycle(5).blend(Group)

        url = reverse('api:groups-list')
        response = api_adm_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 5

        url = reverse('api:groups-detail', kwargs={'pk': groups[0].pk})
        response = api_adm_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == groups[0].name

    def test_update(self, api_adm_client):
        group = mixer.blend(Group, name='Bad Users')

        url = reverse('api:groups-detail', kwargs={'pk': group.pk})
        response = api_adm_client.patch(url, {'name': 'Premium'})
        assert response.status_code == status.HTTP_200_OK

        group.refresh_from_db()
        assert group.name == 'Premium'

    def test_delete(self, api_adm_client):
        group = mixer.blend(Group, name='Full Experience')

        url = reverse('api:groups-detail', kwargs={'pk': group.pk})
        response = api_adm_client.delete(url, follow=True)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Group.objects.filter(pk=group.pk).exists()
