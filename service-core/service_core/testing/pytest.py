import os

import pytest
from testfixtures import LogCapture


def _include_env_arg(arg, args, envname):
    env = os.environ.get(envname, None)
    if not any(arg in s for s in args) and env:
        args += ['{0}={1}'.format(arg, env)]


def pytest_cmdline_preparse(config, args):
    _include_env_arg('--amqp-uri', args, 'AMQP_URI')
    _include_env_arg('--rabbit-ctl-uri', args, 'RABBITMQ_CTL_URI')


@pytest.fixture
def config(rabbit_config):
    return {
        **rabbit_config,
        'DEBUG': True,
    }


@pytest.fixture(autouse=True)
def logs(request):
    names = getattr(request, 'param', None)
    with LogCapture(names=names) as capture:
        yield capture
