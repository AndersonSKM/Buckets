import pytest
from mock import Mock, patch

from core import services


@pytest.mark.django_db
@patch('core.services.User')
class TestSeedE2ETestsData:
    def test_create_user_if_not_exists(self, mock_user_model):
        mock_user_model.objects.get_or_none.return_value = None
        services.seed_e2e_user()

        mock_user_model.objects.create_user.assert_called_once_with(
            email='john.doe@test.com',
            password='johndoe',
            name='John Doe'
        )

    def test_delete_and_create_user_if_exists(self, mock_user_model):
        mock_user = Mock()
        mock_user_model.objects.get_or_none.return_value = mock_user
        services.seed_e2e_user()

        assert mock_user.delete.called
        assert mock_user_model.objects.create_user.called

    def test_just_delete_when_created_param_is_false(self, mock_user_model):
        mock_user = Mock()
        mock_user_model.objects.get_or_none.return_value = mock_user
        result = services.seed_e2e_user(create=False)

        assert result is None
        assert mock_user.delete.called
        assert not mock_user_model.objects.create_user.called


@pytest.mark.django_db
class TestCheckDatabaseState:
    def test_successfully(self, django_assert_max_num_queries):
        with django_assert_max_num_queries(1):
            services.check_database_state()

    @patch('django.db.backends.utils.CursorWrapper.__enter__')
    def test_raise_exception_when_db_fails(self, mock_cursor):
        mock_cursor.return_value.fetchone.return_value = None
        with pytest.raises(Exception) as error:
            services.check_database_state()

        assert str(error.value) == 'Database is not working: Invalid DB response'


class TestCheckCacheState:
    def test_successfully(self):
        services.check_cache_state()

    @patch('core.services.cache')
    def test_raise_exception_when_cache_fails(self, mock_cache):
        mock_cache.get.return_value = None
        with pytest.raises(Exception) as error:
            services.check_cache_state()

        assert str(error.value) == "Cache is not working: Invalid Cache response"
