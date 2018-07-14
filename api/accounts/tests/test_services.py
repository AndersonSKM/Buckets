import pytest
from django.urls import resolve
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
from mock import Mock, patch
from testfixtures import should_raise

from accounts.services import (
    activate_user,
    send_user_activation_email,
    user_activation_info,
    user_from_uuidb64,
)
from accounts.utils import user_activation_token


class TestUserServices:
    @pytest.fixture
    def info(self, user):
        return user_activation_info(user)

    def test_user_from_uuidb64_valid_uuid(self, user):
        uuid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        user_pk = user_from_uuidb64(uuid).pk
        assert user_pk == user.pk

    def test_user_from_uuidb64_invalid_uuid(self, user):
        assert not user_from_uuidb64('123891ui2')

    def test_user_activation_info(self, info, user):
        assert 4 == len(info)
        assert user.get_full_name() == info.get('user_full_name')
        assert user_from_uuidb64(info.get('uuid'))
        assert user_activation_token.check_token(user, info.get('token'))
        assert resolve(info.get('uri'))

    @should_raise(ValueError("Invalid activation parameters"))
    def test_activate_user_with_invalid_uuid(self, info):
        activate_user('test', info['token'])

    @should_raise(ValueError("Invalid activation parameters"))
    def test_activate_with_invalid_token(self, info):
        activate_user(info['uuid'], '12312s')

    @patch('accounts.services.user_activation_token')
    @patch('accounts.services.user_from_uuidb64')
    def test_activate_user_with_active_user(self, mock_uuid, mock_token, info):
        user = Mock(is_active=True)
        mock_uuid.return_value = user
        mock_token.check_token.return_value = True

        activate_user(info['uuid'], info['token'])
        assert not user.save.called

    def test_activate_user_with_inactive_user(self, user_model):
        user = mixer.blend(user_model, is_active=False)
        info = user_activation_info(user)
        activate_user(info['uuid'], info['token'])

        user.refresh_from_db()
        assert user.is_active

    @patch('accounts.services.render_to_string')
    def test_send_user_activation_email(self, mock_render, user_model, mailoutbox):
        user = mixer.blend(user_model, is_active=False)
        send_user_activation_email(user)

        args, _ = mock_render.call_args_list[0]
        assert args[0] == 'activation_email.html'
        assert 'user_full_name' in args[1]
        assert 'uri' in args[1]
        assert 'uuid' in args[1]
        assert 'token' in args[1]

        assert 1 == len(mailoutbox)
        email = mailoutbox[0]

        assert "Activate your account" == email.subject
        assert 1 == len(email.to)
        assert user.email == email.to[0]

    @should_raise(ValueError("User already active"))
    def test_send_activation_email_active_user(self):
        mock_user = Mock(is_active=True)
        send_user_activation_email(mock_user)
