import logging

from nameko.extensions import DependencyProvider
from sendgrid import SendGridAPIClient

SENDGRID_API_KEY = 'SENDGRID_API_KEY'


class SendGrid(DependencyProvider):
    def __init__(self, **kwargs):
        self.client = None
        self.key = None
        super(SendGrid, self).__init__(**kwargs)

    def setup(self):
        self.key = self.container.config['SENDGRID_API_KEY']
        self.client = SendGridAPIClient(apikey=self.key)

    def get_dependency(self, worker_ctx):
        return self.client


class Logger(DependencyProvider):
    def __init__(self, **kwargs):
        self.logger = None
        super(Logger, self).__init__(**kwargs)

    def setup(self):
        self.logger = logging.getLogger(self.container.service_name)

    def get_dependency(self, worker_ctx):
        return self.logger
