import logging

import pytest
from mock import Mock
from nameko.containers import ServiceContainer
from sendgrid import SendGridAPIClient

from service_core.dependency_providers import (
    SENDGRID_API_KEY,
    Logger,
    SendGrid,
)


@pytest.fixture
def config(config):
    return {
        **config,
        SENDGRID_API_KEY: 'secret'
    }


@pytest.fixture
def container(config):
    return Mock(
        spec=ServiceContainer, config=config, service_name='example'
    )


@pytest.fixture
def sendgrid_provider(container):
    return SendGrid().bind(container, 'sendgrid')


@pytest.fixture
def logger_provider(container):
    return Logger().bind(container, 'logger')


class TestSendgrid:
    def test_setup(self, sendgrid_provider, config):
        assert not sendgrid_provider.client
        assert not sendgrid_provider.key

        sendgrid_provider.setup()
        dependency = sendgrid_provider.get_dependency(None)
        assert isinstance(dependency, SendGridAPIClient)
        assert dependency.apikey == config[SENDGRID_API_KEY]


class TestLogger:
    def test_setup(self, logger_provider, container):
        assert not logger_provider.logger

        logger_provider.setup()
        dependency = logger_provider.get_dependency(None)
        assert isinstance(dependency, logging.Logger)
        assert dependency.name == container.service_name
