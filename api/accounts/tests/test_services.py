from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
from mock import Mock, patch
from testfixtures import should_raise

from accounts.services import send_user_activation_email, user_activation_link, user_from_uuidb64


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
        settings.USER_ACTIVATION_URI = 'app.com/{uuidb64}/{token}/'
        mock_uuid.return_value = '1234'
        mock_token.return_value = '5678'
        assert user_activation_link(user) == 'app.com/1234/5678/'

    @should_raise(ImproperlyConfigured("No activation URI specified."))
    def test_user_activation_link_invalid_uri(self, settings, user):
        settings.USER_ACTIVATION_URI = None
        user_activation_link(user)

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

        assert 1 == len(mailoutbox)
        email = mailoutbox[0]

        assert "Activate your account" == email.subject
        assert 1 == len(email.to)
        assert user.email == email.to[0]

    @should_raise(ValueError("User already active."))
    def test_send_activation_email_active_user(self):
        mock_user = Mock(is_active=True)
        send_user_activation_email(mock_user)
