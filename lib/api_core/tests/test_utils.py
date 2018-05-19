from decimal import Decimal

import pytest
from mixer.backend.django import mixer

from core.utils.models import to_dict
from tests.models import Chef, Ingredient, Recipe


@pytest.mark.django_db
@pytest.mark.freeze_time('2018-01-04 18:00:00')
class TestHelpers:
    data = {
        'id': '2e55d121-6132-449a-8788-5fa0a99bb550',
        'updated_at': '2018-01-04 18:00:00',
        'created_at': '2018-01-04',
        'deleted_at': None,
        'user': 'anderson.krs95@gmail.com',
        'name': 'Chicken Ribs',
        'chef': '88e70bee-fe06-4e45-8c8b-d21ff3f6777c',
        'ingredients': [
            '4063a315-3a6a-4c40-85e7-eec524f99222',
            '979e401e-b124-434a-9ac0-a8042d15f4c2',
            'ed7b7bff-8fc8-47b2-b6cc-7d69cad9da45'
        ],
        'vegan': True,
        'picture': '/media/image.gif',
        'country': None,
        'time_to_cook': '18:00:00',
        'pounds': 10,
        'price': 1.99
    }

    def test_model_instance_to_dict(self):
        chef = mixer.blend(Chef, pk=self.data['chef'])
        ingredients = mixer.cycle(3).blend(
            Ingredient,
            pk=(id for id in self.data['ingredients'])
        )

        fields = {
            **self.data,
            'ingredients': ingredients,
            'chef': chef,
            'price': Decimal('1.99'),
            'picture': 'image.gif',
        }

        recipe = mixer.blend(Recipe, **fields)
        assert to_dict(recipe, exclude=['short_name']) == self.data
