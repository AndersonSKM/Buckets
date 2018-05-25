import os

import mock

from service_core.testing.pytest import config, pytest_cmdline_preparse


class TestPytestPlugin:
    @mock.patch.dict(os.environ, {
        'AMQP_URI': 'amqp://test',
        'RABBITMQ_CTL_URI': 'http://test',
    })
    def test_include_env_arg_without_args(self):
        args = list()
        pytest_cmdline_preparse(None, args)
        assert '--amqp-uri=amqp://test' in args
        assert '--rabbit-ctl-uri=http://test' in args

    @mock.patch.dict(os.environ, {
        'AMQP_URI': 'amqp://test2',
        'RABBITMQ_CTL_URI': 'http://test2',
    })
    def test_include_env_arg_with_args(self):
        args = ['--amqp-uri=amqp://test1', '--rabbit-ctl-uri=http://test1']
        pytest_cmdline_preparse(None, args)
        assert args[0] == '--amqp-uri=amqp://test1'
        assert args[1] == '--rabbit-ctl-uri=http://test1'

    @mock.patch.dict(os.environ, {
        'AMQP_URI': '',
        'RABBITMQ_CTL_URI': '',
    })
    def test_include_env_arg_without_env(self):
        args = list()
        pytest_cmdline_preparse(None, args)
        assert not args

    def test_config(self, rabbit_config):
        assert config(rabbit_config) == {**rabbit_config, 'DEBUG': True}
