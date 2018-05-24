from rest_framework.serializers import ModelSerializer

from core.tests.models import Chef

# Dummy serializers, just for testing


class ChefSerializer(ModelSerializer):
    class Meta:
        model = Chef
        fields = ('pk', 'name')
