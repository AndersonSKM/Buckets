from django.shortcuts import render
from django.views.decorators.cache import never_cache
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core import services


@never_cache
def index(request):
    return render(request, 'index.html')


class HeathCheckView(views.APIView):
    permission_classes = [AllowAny,]
    throttle_scope = 'health-check'

    def get(self, request, *args, **kwargs):
        services.check_database_state()
        services.check_cache_state()
        return Response(status=status.HTTP_200_OK, data={'detail': 'healthy'})


class SeedE2ETestsDataView(views.APIView):
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        services.seed_e2e_user()
        return Response(status=status.HTTP_201_CREATED)
