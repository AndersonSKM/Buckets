import pytest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import mixer
from mock import Mock, patch
from testfixtures import should_raise

from accounts.services import UserService


class TestUserService:
    @pytest.fixture
    def info(self, user):
        return UserService.activation_info(user)

    def test_user_from_uuidb64_valid_uuid(self, user):
        uuid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        user_pk = UserService.user_from_uuidb64(uuid).pk
        assert user_pk == user.pk

    def test_user_from_uuidb64_invalid_uuid(self, user):
        assert not UserService.user_from_uuidb64('123891ui2')

    def test_activation_info(self, info, user):
        assert user.get_full_name() == info.get('user_full_name')
        assert isinstance(info['user_full_name'], str)
        assert info.get('uuid')
        assert isinstance(info['uuid'], str)
        assert info.get('token')
        assert isinstance(info['token'], str)
        assert info.get('uri')
        assert isinstance(info['uri'], str)

    @should_raise(ValueError("Invalid activation parameters"))
    def test_activate_with_invalid_uuid(self, info):
        UserService.activate('test', info['token'])

    @should_raise(ValueError("Invalid activation parameters"))
    def test_activate_with_invalid_token(self, info):
        UserService.activate(info['uuid'], '12312s')

    @patch('accounts.services.user_activation_token')
    @patch('accounts.services.UserService.user_from_uuidb64')
    def test_activate_with_active_user(self, mock_uuid, mock_token, info):
        user = Mock(is_active=True)
        mock_uuid.return_value = user
        mock_token.check_token.return_value = True

        UserService.activate(info['uuid'], info['token'])
        assert not user.save.called

    def test_activate_with_inactive_user(self, user_model):
        user = mixer.blend(user_model, is_active=False)
        info = UserService.activation_info(user)
        UserService.activate(info['uuid'], info['token'])
        user.refresh_from_db()
        assert user.is_active

    @patch('accounts.services.render_to_string')
    def test_send_activation_email(self, mock_render, user_model, mailoutbox):
        user = mixer.blend(user_model, is_active=False)
        UserService.send_activation_email(user)

        args, _ = mock_render.call_args_list[0]
        assert args[0] == 'activation_email.html'

        assert 1 == len(mailoutbox)
        email = mailoutbox[0]
        assert "Activate your account" == email.subject

    @should_raise(ValueError("User already active"))
    def test_send_activation_email_active_user(self):
        mock_user = Mock(is_active=True)
        UserService.send_activation_email(mock_user)
