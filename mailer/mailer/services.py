import logging

from nameko.dependency_providers import Config
from nameko.events import BROADCAST
from nameko_amqp_retry import entrypoint_retry
from nameko_amqp_retry.events import event_handler
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Content,
    Email,
    Mail,
    MailSettings,
    SandBoxMode,
)


class MailerService:
    name = 'mailer'
    config = Config()

    def __init__(self):
        self.api = SendGridAPIClient()

    @event_handler(
        'global', 'send_mail', handler_type=BROADCAST, reliable_delivery=False
    )
    @entrypoint_retry(schedule=(60000,))
    def send_mail(self, payload):
        from_email = Email(payload['from_email'])
        to_email = Email(payload['to_email'])
        subject = payload['subject']
        content = Content('text/plain', payload['content'])

        mail = self._setup_mail(from_email, subject, to_email, content)
        try:
            self._pre_send(mail)

            response = self._internal_send(mail)
            self._post_send(response)
        except HTTPError as e:
            self._send_error(e)
            raise

    def _setup_mail(self, from_email, subject, to_email, content):
        mail = Mail(from_email, subject, to_email, content)
        mail.mail_settings = MailSettings()
        mail.mail_settings.sandbox_mode = SandBoxMode(
            enable=self.config['DEBUG']
        )
        return mail.get()

    def _internal_send(self, mail):
        if not self.api.api_key:
            self.api.api_key = self.config['API_KEY']
        return self.api.client.mail.send.post(request_body=mail)

    def _pre_send(self, mail):
        log_str = "Attempting to send email - Message: {msg}".format(msg=mail)
        logging.info(log_str)

    def _post_send(self, response):
        log_str = (
            "Received response from Sendgrid - "
            "Status: {status} - Message: {msg}"
        ).format(
            status=response.status_code,
            msg=response.body,
        )
        logging.info(log_str)

    def _send_error(self, e):
        log_str = (
            "HTTP Error from Sendgrid - "
            "Status Code: {status_code} - "
            "Reason: {reason} - "
            "Message: {body}"
        ).format(
            status_code=e.status_code,
            reason=e.reason,
            body=e.to_dict,
        )
        logging.error(log_str)
