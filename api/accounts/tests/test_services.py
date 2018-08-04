from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
from mock import Mock, patch
from rest_framework.exceptions import ValidationError
from testfixtures import should_raise

from accounts.services import (
    send_user_activation_email,
    send_user_password_reset_email,
    user_activation_link,
    user_from_uuidb64,
    user_password_reset_link,
)


class TestUserServices:
    def test_user_from_uuidb64_valid_uuid(self, user):
        uuid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        user_pk = user_from_uuidb64(uuid).pk
        assert user_pk == user.pk

    def test_user_from_uuidb64_invalid_uuid(self, user):
        assert not user_from_uuidb64('123891ui2')

    @patch('accounts.services.user_activation_token.make_token')
    @patch('accounts.services.encode_user_uuid')
    def test_user_activation_link(self, mock_uuid, mock_token, settings, user):
        settings.USER_ACTIVATION_URI = 'app.com/activate/{uuidb64}/{token}/'
        mock_uuid.return_value = '1234'
        mock_token.return_value = '5678'
        assert user_activation_link(user) == 'app.com/activate/1234/5678/'

    @should_raise(ImproperlyConfigured("No activation URI specified."))
    def test_user_activation_link_invalid_uri(self, settings, user):
        settings.USER_ACTIVATION_URI = None
        user_activation_link(user)

    @patch('accounts.services.default_token_generator.make_token')
    @patch('accounts.services.encode_user_uuid')
    def test_user_password_reset_link(self, mock_uuid, mock_token, settings, user):
        settings.USER_PASSWORD_RESET_URI = 'app.com/password-reset/{uuidb64}/{token}/'
        mock_uuid.return_value = 'ABC1'
        mock_token.return_value = 'EFG6'
        assert user_password_reset_link(user) == 'app.com/password-reset/ABC1/EFG6/'

    @should_raise(ImproperlyConfigured("No reset password URI specified."))
    def test_user_password_reset_link_invalid_uri(self, settings, user):
        settings.USER_PASSWORD_RESET_URI = None
        user_password_reset_link(user)

    @patch('accounts.services.user_activation_link')
    @patch('accounts.services.render_to_string')
    def test_send_user_activation_email(self, mock_render, mock_link, user_model, mailoutbox):
        mock_link.return_value = 'fakelink'
        user = mixer.blend(user_model, is_active=False)
        send_user_activation_email(user)

        args, _ = mock_render.call_args_list[0]
        assert args[0] == 'activation_email.html'
        assert args[1].get('user') == user
        assert args[1].get('activation_link') == 'fakelink'

        assert len(mailoutbox) == 1
        email = mailoutbox[0]

        assert "Activate your account" == email.subject
        assert email.to == [user.email]

    @patch('accounts.services.user_password_reset_link')
    @patch('accounts.services.render_to_string')
    def test_send_user_password_reset_email(self, mock_render, mock_link, user_model, mailoutbox):
        mock_link.return_value = 'fakelink'
        user = mixer.blend(user_model, is_active=True)
        send_user_password_reset_email(user)

        args, _ = mock_render.call_args_list[0]
        assert args[0] == 'password_reset_email.html'
        assert args[1].get('user') == user
        assert args[1].get('password_reset_link') == 'fakelink'

        assert len(mailoutbox) == 1
        email = mailoutbox[0]

        assert "Reset your password" == email.subject
        assert email.to == [user.email]

    @should_raise(ValidationError("User already active."))
    def test_send_activation_email_active_user(self):
        mock_user = Mock(is_active=True)
        send_user_activation_email(mock_user)

    @should_raise(ValidationError("User isn't already active."))
    def test_send_user_password_reset_email_inactive_user(self):
        mock_user = Mock(is_active=False)
        send_user_password_reset_email(mock_user)
