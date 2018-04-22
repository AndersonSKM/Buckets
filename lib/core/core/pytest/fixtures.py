import json
import os

import pytest
from django.contrib.auth.models import AnonymousUser
from mixer.backend.django import mixer
from rest_framework.request import Request
from rest_framework.test import APIClient, APIRequestFactory


@pytest.fixture()
def user_model(request, django_user_model):
    return django_user_model


@pytest.fixture()
def adm_user(request, user_model):
    """
    This fixture will return a django admin user
    """
    return mixer.blend(user_model, is_superuser=True, is_staff=True)


@pytest.fixture()
def user(request, user_model):
    """
    This fixture will return a django user
    """
    return mixer.blend(user_model, is_superuser=False, is_staff=False)


@pytest.fixture()
def anon_user(request):
    """
    This fixture will return a django anonymous user
    """
    return AnonymousUser()


@pytest.fixture()
def api_client(request):
    """
    REST framework API client
    This fixture will return a client
    """
    return APIClient()


@pytest.fixture()
def api_auth_client(request, api_client, user):
    """
    REST framework API client
    This fixture will return a client logged
    """
    api_client.force_authenticate(user)
    return api_client


@pytest.fixture()
def api_adm_client(request, api_client, adm_user):
    """
    REST framework API client
    This fixture will return a client logged by adm user
    """
    api_client.force_authenticate(adm_user)
    return api_client


@pytest.fixture()
def api_factory(request):
    """
    DJANGO Request Factory
    This fixture will return a request django factory
    """
    return APIRequestFactory()


@pytest.fixture()
def rootdir(request):
    """
    This fixture will return the pytest root dir
    """
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture()
def rjson(request, rootdir):
    """
    This fixture will return a function to read json files
    """
    def read(file):
        data = open(os.path.join(rootdir, file)).read()
        return json.loads(data)
    return read


@pytest.fixture()
def serializer_context(request, api_factory):
    """
    This fixture will return a fake serialize request fro uri fields
    """
    request = api_factory.get('/')
    return {
        'request': Request(request),
    }
