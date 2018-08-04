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

    @patch('django.db.backends.utils.CursorWrapper.__enter__')
    def test_database_response_error(self, mock_cursor, anonymous_client, url):
        mock_cursor.return_value.fetchone.return_value = None
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {'detail': 'Database is not working: Invalid DB response'}

    @patch('core.views.cache')
    def test_cache_response_error(self, mock_cache, anonymous_client, url):
        mock_cache.get.return_value = None
        response = anonymous_client.get(path=url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data == {'detail': 'Cache is not working: Invalid Cache response'}
