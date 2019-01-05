import pytest
from django.urls import reverse
from mock import patch
from rest_framework import status


class TestHealthCheckView:
    @pytest.fixture
    def url(self):
        return reverse('core:health-check')

    def test_successful(self, anonymous_client, url):
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {'detail': 'healthy'}

    @patch('core.views.services')
    def test_database_response_error(self, mock_services, anonymous_client, url):
        mock_services.check_database_state.side_effect = Exception('Error')
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {'detail': 'Error'}

    @patch('core.views.services')
    def test_cache_response_error(self, mock_services, anonymous_client, url):
        mock_services.check_cache_state.side_effect = Exception('Error')
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {'detail': 'Error'}
