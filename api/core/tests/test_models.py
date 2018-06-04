import pytest
from django.contrib.contenttypes.models import ContentType
from mixer.backend.django import mixer

from core.models import DBActions, Revision
from core.tests.models import Chef, Ingredient, Recipe


@pytest.mark.django_db
class TestRevision:
    @pytest.fixture
    def data(self):
        return {
            'fields': {
                'chef': 'c031bab9-1f9d-4168-8be1-02453a57f08c',
                'country': None,
                'created_at': '2018-03-28',
                'ingredients': [
                    '647e0949-adf6-46c3-8316-da5d5f850377',
                ],
                'name': 'Aaron Hernandez',
                'picture': 'image_sv2C3pM.gif',
                'pounds': 7632,
                'price': '332.49',
                'short_name': 'ZuhevIEMJF',
                'time_to_cook': '12:43:48',
                'updated_at': '2018-03-28T12:43:48',
                'user': 'eramirez@hotmail.com',
                'vegan': True,
            },
            'model': 'core.recipe',
            'pk': '0bb9f04d-d0bd-4490-9fe8-cad43f9cdf83',
        }

    def test_delete_instance(self):
        chef = mixer.blend(Chef)
        chef.delete()
        assert chef._state.destroing

    def test_init_without_instance(self):
        rev = Revision()
        assert not rev.content_type_id
        assert not rev.user
        assert not rev.action
        assert not rev.data

    @pytest.mark.freeze_time('2018-03-28 12:43:48')
    def test_init_with_instance(self, data, settings):
        settings.USE_TZ = False

        fields = data['fields'].copy()
        chef = mixer.blend(Chef, pk=fields.pop('chef'))
        ingredient = mixer.blend(Ingredient, pk=fields.pop('ingredients')[0])
        fields = {
            **fields,
            'pk': data['pk'],
            'chef': chef,
            'ingredients': (ingredient,),
        }

        recipe = mixer.blend(Recipe, **fields)
        rev = Revision.objects.create(instance=recipe)
        content_type = ContentType.objects.get_for_model(recipe)

        assert rev.data == data
        assert rev.user == data['fields']['user']
        assert rev.action == DBActions.UPDATE
        assert rev.content_type == content_type

    def test_instance_user_without_user_field(self):
        obj = mixer.blend(Ingredient)
        rev = Revision()
        assert not rev._instance_user(obj)

    def test_instance_user_with_user_field(self):
        obj = mixer.blend(Chef)
        rev = Revision()
        assert rev._instance_user(obj) == obj.user

    def test_instance_action(self):
        obj = Chef()
        rev = Revision()

        obj._state.adding = True
        assert rev._instance_action(obj) == DBActions.CREATE

        obj._state.adding = False
        assert rev._instance_action(obj) == DBActions.UPDATE

        obj._state.destroing = True
        assert rev._instance_action(obj) == DBActions.DESTROY
