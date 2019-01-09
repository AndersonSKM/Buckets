import pytest
from django.http import HttpResponse
from django.test import Client as DjangoClient
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from mock import patch
from rest_framework import status

from core.views import SeedE2ETestsDataView


class TestIndexPage:
    @pytest.fixture
    def url(self):
        return reverse('core:index')

    @pytest.fixture
    def client(self):
        return DjangoClient()

    @patch('core.views.render')
    def test_successfully(self, mock_render, client, url):
        mock_render.return_value = HttpResponse(status=status.HTTP_200_OK)
        response = client.get(path=url)

        assert mock_render.called
        assert response.status_code == status.HTTP_200_OK


class TestHealthCheck:
    @pytest.fixture
    def url(self):
        return reverse('core:health-check')

    def test_successfully(self, anonymous_client, url):
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'detail': 'healthy'}

    @patch('core.views.services')
    def test_error_when_database_is_not_working(self, mock_services, anonymous_client, url):
        mock_services.check_database_state.side_effect = Exception('DB Error')
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {'detail': 'DB Error'}

    @patch('core.views.services')
    def test_error_when_cache_is_not_working(self, mock_services, anonymous_client, url):
        mock_services.check_cache_state.side_effect = Exception('Cache Error')
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {'detail': 'Cache Error'}


class TestSeedE2EData:
    def test_successfully(self, factory, settings, user_model):
        request = factory.post('/api/seed/', format='json')
        view = SeedE2ETestsDataView.as_view()
        response = view(request)

        assert response.status_code == status.HTTP_201_CREATED
        assert user_model.objects.get_by_natural_key('john.doe@test.com')

    def test_endpoint_not_found_running_in_production(self):
        with pytest.raises(NoReverseMatch):
            reverse('core:seed-db')
