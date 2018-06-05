import pytest
from mixer.backend.django import mixer

from core.models import Revision
from core.tests.models import Recipe


@pytest.mark.django_db
class TestRevisionManagerMixin:
    def test_revision_model(self):
        assert Recipe.objects.revision_model is Revision

    def test_content_type(self):
        content_type = Recipe.objects.content_type
        assert content_type
        assert content_type.model_class() == Recipe

    def test_revisions(self):
        parmegiana = mixer.blend(Recipe)
        tiramisu = mixer.blend(Recipe)

        revisions = Recipe.objects.revisions(parmegiana)
        assert len(revisions) == 1
        assert revisions.first().data['pk'] == str(parmegiana.pk)

        revisions = Recipe.objects.revisions(tiramisu)
        assert len(revisions) == 1
        assert revisions.first().data['pk'] == str(tiramisu.pk)


@pytest.mark.django_db
class TestAbstractBaseManager:
    def test_get_or_none(self):
        obj = mixer.blend(Recipe)
        fake_uuid = '007102db-a6c0-4aef-a901-b50a1457b9af'
        assert Recipe.objects.get_or_none(pk=obj.pk)
        assert not Recipe.objects.get_or_none(pk=fake_uuid)


@pytest.mark.django_db
class TestBaseManager:
    def test_from_user(self, user, adm_user):
        obj_user = mixer.blend(Recipe, user=user)
        obj_adm = mixer.blend(Recipe, user=adm_user)
        assert Recipe.objects.all().count() == 2

        qs = Recipe.objects.from_user(user)
        assert qs.count() == 1
        assert obj_user in qs

        qs = Recipe.objects.from_user(adm_user)
        assert qs.count() == 1
        assert obj_adm in qs
