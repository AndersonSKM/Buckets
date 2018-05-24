from rest_framework.viewsets import ModelViewSet

from core.permissions import AnonCreateUserUpdateSelfOnly, ListUserAdminOnly
from core.tests.models import Chef
from core.tests.serializers import ChefSerializer

# Dummy views, just for testing


class ChefViewSet(ModelViewSet):
    serializer_class = ChefSerializer
    queryset = Chef.objects.all()
    permission_classes = (
        AnonCreateUserUpdateSelfOnly,
        ListUserAdminOnly,
    )
