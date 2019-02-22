import logging

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import connection, transaction

logger = logging.getLogger(__name__)
User = get_user_model()


@transaction.atomic
def seed_e2e_user():
    user = User.objects.get_or_none(email='john.doe@test.com')
    if user:
        user.delete()
    return User.objects.create_user(
        email='john.doe@test.com',
        password='johndoe',
        name='John Doe',
    )


def check_database_state():
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1;')
            row = cursor.fetchone()
            if not row:
                raise Exception("Invalid DB response")
    except Exception as error:
        logger.exception(error)
        raise Exception(f"Database is not working: {error}")


def check_cache_state():
    try:
        cache.set('alive', True, timeout=None)
        if not cache.get('alive'):
            raise Exception("Invalid Cache response")
    except Exception as error:
        logger.exception(error)
        raise Exception(f"Cache is not working: {error}")
