import logging

from django.core.cache import cache
from django.db import connection
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from rest_framework import status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

logger = logging.getLogger(__name__)


@method_decorator(never_cache, name='dispatch')
class IndexView(TemplateView):
    template_name = 'index.html'


class HeathCheckView(views.APIView):
    permission_classes = [AllowAny,]
    throttle_scope = 'health-check'

    def get(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1;')
                row = cursor.fetchone()
                if not row:
                    raise Exception("Invalid DB response")
        except Exception as error:
            logger.exception(error)
            raise Exception(f"Database is not working: {error}")

        try:
            cache.set('alive', True, timeout=None)
            if not cache.get('alive'):
                raise Exception("Invalid Cache response")
        except Exception as error:
            logger.exception(error)
            raise Exception(f"Cache is not working: {error}")

        return Response(status=status.HTTP_200_OK, data={'detail': 'healthy'})
