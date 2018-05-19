import pytest
from mixer.backend.django import mixer

from tests.models import Recipe


@pytest.mark.django_db
class TestAbstractBaseManager:
    def test_full(self):
        mixer.cycle(5).blend(Recipe)
        assert Recipe.objects.full().count() == Recipe.objects.all().count()

        obj = Recipe.objects.all().first()
        obj.delete()

        assert Recipe.objects.all().count() == 4
        assert obj not in Recipe.objects.all().active()

        assert Recipe.objects.full().count() == 5
        assert obj in Recipe.objects.full()


@pytest.mark.django_db
class TestBaseManager:
    def test_from_user(self, user, adm_user):
        obj_user = mixer.blend(Recipe, user=user.email)
        obj_adm = mixer.blend(Recipe, user=adm_user.email)
        assert Recipe.objects.all().count() == 2

        qs = Recipe.objects.from_user(user.email)
        assert qs.count() == 1
        assert obj_user in qs

        qs = Recipe.objects.from_user(adm_user.email)
        assert qs.count() == 1
        assert obj_adm in qs
