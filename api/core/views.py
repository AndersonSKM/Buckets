import logging

from django.core.cache import cache
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

logger = logging.getLogger(__name__)


class HealthCheckThrottle(AnonRateThrottle):
    rate = '60/minute'


@api_view(['GET',])
@permission_classes([AllowAny,])
@throttle_classes([HealthCheckThrottle,])
def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1;')
            row = cursor.fetchone()
            if not row:
                raise Exception("Invalid DB response")
    except Exception as error:
        logger.exception(error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
            'detail': f"Database is not working: {error}"}
        )

    try:
        cache.set('alive', True, timeout=None)
        if not cache.get('alive'):
            raise Exception("Invalid Cache response")
    except Exception as error:
        logger.exception(error)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
            'detail': f"Cache is not working: {error}"}
        )

    return Response(status=status.HTTP_200_OK, data={'detail': 'healthy'})
