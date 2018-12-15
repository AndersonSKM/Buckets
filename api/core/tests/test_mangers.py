import pytest
from mixer.backend.django import mixer


@pytest.mark.django_db
class TestAbstractBaseManager:
    def test_get_or_none_invalid_query(self, user_model):
        fake_uuid = '007102db-a6c0-4aef-a901-b50a1457b9af'
        assert not user_model.objects.get_or_none(pk=fake_uuid)

    def test_get_or_none_valid_query(self, user_model):
        instance = mixer.blend(user_model)
        assert user_model.objects.get_or_none(pk=instance.pk)
