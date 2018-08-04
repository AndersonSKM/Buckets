import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


@pytest.fixture
def user_model(django_user_model):
    return django_user_model


@pytest.fixture
def adm_user(user_model):
    """
    This fixture will return a django admin user
    """
    return mixer.blend(
        user_model,
        email='admin@admin.com',
        is_active=True,
        is_superuser=False,
        is_staff=True
    )


@pytest.fixture
def user(user_model):
    """
    This fixture will return a django user
    """
    return mixer.blend(
        user_model,
        email='user@user.com',
        is_active=True,
        is_superuser=False,
        is_staff=False
    )


@pytest.fixture
def anon_user():
    """
    This fixture will return a django anonymous user
    """
    return AnonymousUser()


@pytest.fixture
def jwt():
    def execute(instance):
        payload = jwt_payload_handler(instance)
        return jwt_encode_handler(payload)
    return execute


@pytest.fixture
def anonymous_client(user, jwt):
    """REST framework API client"""
    return APIClient()


@pytest.fixture
def client(anonymous_client, user, jwt):
    """
    REST framework API client
    This fixture will return a client logged
    """
    token = jwt(user)
    anonymous_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
    return anonymous_client


@pytest.fixture
def adm_client(anonymous_client, adm_user, jwt):
    """
    REST framework API client
    This fixture will return a client logged by adm user
    """
    token = jwt(adm_user)
    anonymous_client.credentials(HTTP_AUTHORIZATION=f'JWT {token}')
    return anonymous_client


@pytest.fixture
def factory():
    """
    DJANGO Request Factory
    This fixture will return a request django factory
    """
    return APIRequestFactory()


@pytest.fixture
def serializer_context(factory):
    """
    This fixture will return a fake serialize request for uri fields
    """
    request = factory.get('/')
    return {
        'request': Request(request),
    }
