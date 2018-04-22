import pytest
from django.utils import timezone
from mixer.backend.django import mixer

from tests.models import Chef


@pytest.mark.django_db
class TestBaseQuerySet:
    def test_delete(self):
        mixer.cycle(3).blend(Chef)
        Chef.objects.all().delete()
        assert Chef.objects.all().count() == 0
        for obj in Chef.objects.full():
            assert obj.deleted_at

    def test_undelete(self):
        mixer.cycle(3).blend(Chef, deleted_at=timezone.now())
        Chef.objects.full().undelete()
        assert Chef.objects.all().count() == 3
        for obj in Chef.objects.all():
            assert not obj.deleted_at

    def test_active_deleted(self):
        mixer.cycle(3).blend(Chef, deleted_at=timezone.now())
        mixer.cycle(2).blend(Chef, deleted_at=None)
        assert Chef.objects.full().active().count() == 2
        assert Chef.objects.full().deleted().count() == 3

    def test_destroy(self):
        mixer.cycle(3).blend(Chef, deleted_at=None)
        Chef.objects.all().destroy()
        assert Chef.objects.all().count() == 0
        assert Chef.objects.full().count() == 0
