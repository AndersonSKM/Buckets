import pytest
from django.utils import timezone
from mixer.backend.django import mixer
from testfixtures import should_raise

from core.models import Revision
from tests.models import Chef, Ingredient


@pytest.mark.django_db
class TestAbstractBaseModel:
    def test_delete(self):
        obj = mixer.blend(Chef)
        obj.delete()
        assert obj.deleted_at

    def test_undelete(self):
        obj = mixer.blend(Chef)
        obj.delete()
        assert obj.deleted_at

        obj.undelete()
        assert not obj.deleted_at

    def test_destroy(self):
        obj = mixer.blend(Chef)
        obj.destroy()
        assert not Chef.objects.full().filter(pk=obj.pk).exists()

    @should_raise(AssertionError)
    def test_invalid_undeletion(self):
        obj = mixer.blend(Chef)
        obj.deleted_at = None
        obj.undelete()

    @should_raise(AssertionError)
    def test_invalid_deletion(self):
        obj = mixer.blend(Chef)
        obj.deleted_at = timezone.now()
        obj.delete()

    def test_is_deleting(self):
        obj = mixer.blend(Chef)
        assert not obj.is_deleting()

        obj.deleted_at = timezone.now()
        assert obj.is_deleting()

    def test_is_undeleting(self):
        obj = mixer.blend(Chef, deleted_at=timezone.now())
        assert not obj.is_undeleting()

        obj.deleted_at = None
        assert obj.is_undeleting()


@pytest.mark.django_db
class TestRevision:
    data = {
        'id': "41147f16-bbde-4aae-97f6-8899a250fd8b",
        'name': 'Alex Atala',
        'user': 'alex@atala.com',
        'created_at': '2018-03-28 12:43:48',
        'updated_at': '2018-03-28 12:43:48',
        'deleted_at': None
    }

    def test_init_without_instance(self):
        rev = Revision()
        assert not rev.serialized_data

    @pytest.mark.freeze_time('2018-03-28 12:43:48')
    def test_init_with_instance(self, settings):
        settings.USE_TZ = False

        obj = mixer.blend(Chef, **self.data)
        rev = Revision.objects.create(instance=obj)

        assert rev.serialized_data
        assert rev.json() == self.data
        assert str(rev.object_pk) == self.data['id']
        assert rev.user == self.data['user']
        assert rev.action == Revision.Actions.UPDATE
        assert rev.object.pk == obj.pk
        assert rev.content_type.pk == obj.content_type_pk

    def test_init_instance_without_user_field(self):
        obj = mixer.blend(Ingredient)
        rev = Revision.objects.create(instance=obj)
        assert not rev.user

    def test_revision_actions(self):
        obj = mixer.blend(Chef)
        rev = Chef.objects.get_revisions(obj.pk)[:1].first()
        assert rev.action == str(Revision.Actions.CREATE)

        obj.name = 'Paola Carosella'
        obj.save()
        rev = Chef.objects.get_revisions(obj.pk)[:1].first()
        assert rev.action == str(Revision.Actions.UPDATE)

        obj.delete()
        rev = Chef.objects.get_revisions(obj.pk)[:1].first()
        assert rev.action == str(Revision.Actions.DELETE)

        obj.undelete()
        rev = Chef.objects.get_revisions(obj.pk)[:1].first()
        assert rev.action == str(Revision.Actions.UNDELETE)

        pk = obj.pk
        obj.destroy()
        rev = Chef.objects.get_revisions(pk)[:1].first()
        assert rev.action == str(Revision.Actions.DESTROY)
