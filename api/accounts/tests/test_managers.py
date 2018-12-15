import pytest
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from mixer.backend.django import Mixer
from mock import Mock, patch

from accounts.models import User

mixer = Mixer(commit=False)


class TestUserManager:
    @pytest.fixture
    def data(self):
        return {
            'email': 'bruce@we.com',
            'password': '|e_Aub*SF.9F',
            'confirm': '|e_Aub*SF.9F',
            'first_name': 'bruce',
            'last_name': 'wayne',
        }

    @pytest.mark.django_db
    def test_create_superuser(self, data, mailoutbox):
        user = User.objects.create_superuser(**data)

        assert user.is_staff
        assert user.is_superuser
        assert user.is_active
        assert len(mailoutbox) == 0

    @pytest.mark.django_db
    def test_get_active_users(self):
        active_user = mixer.blend(User, is_active=True)
        inactive_user = mixer.blend(User, is_active=False)
        active_user.save()
        inactive_user.save()

        results = User.objects.get_active_users()
        assert len(results) == 1
        assert inactive_user not in results
        assert active_user in results

    @pytest.mark.django_db
    def test_get_active_or_none(self):
        user = mixer.blend(User, is_active=True)
        user.save()
        assert User.objects.get_active_or_none(email=user.email)

        user = mixer.blend(User, is_active=False)
        user.save()
        assert not User.objects.get_active_or_none(email=user.email)

    def test_activate_inactive_user(self):
        user = mixer.blend(User, is_active=False)
        user.save = Mock()
        User.objects.activate(user=user)

        assert user.is_active
        assert user.save.called

    def test_activate_active_user(self):
        user = mixer.blend(User, is_active=True)
        user.save = Mock()
        User.objects.activate(user=user)

        assert user.is_active
        assert not user.save.called

    @pytest.mark.django_db
    def test_create_user(self, data, mailoutbox):
        user = User.objects.create_user(**data)

        assert user.email == data['email']
        assert user.first_name == data['first_name']
        assert user.last_name == data['last_name']
        assert user.check_password(data['password'])
        assert not user.is_staff
        assert not user.is_superuser
        assert not user.is_active
        assert len(mailoutbox) == 1

    @pytest.mark.django_db
    def test_create_user_debug_dont_send_email(self, data, settings, mailoutbox):
        settings.DEBUG = True
        user = User.objects.create_user(**data)

        assert user.is_active
        assert len(mailoutbox) == 0

    @pytest.mark.django_db
    def test_get_user_from_uuidb64_valid_uuid(self, user):
        uuidb64 = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        assert User.objects.get_user_from_uuidb64(uuidb64) == user

    @pytest.mark.django_db
    def test_get_user_from_uuidb64_invalid_uuid(self, user):
        assert not User.objects.get_user_from_uuidb64('123891ui2')

    def test_send_activation_email_invalid_config(self, settings):
        user = mixer.blend(User, is_active=False)
        settings.USER_ACTIVATION_URI = None
        with pytest.raises(ImproperlyConfigured) as error:
            User.objects.send_activation_email(user=user)
            assert error.message == "No activation URI specified."

    def test_send_activation_email_active_user(self):
        user = mixer.blend(User, is_active=True)
        with pytest.raises(ValidationError) as error:
            User.objects.send_activation_email(user=user)
            assert error.message == "User already active."

    @patch('accounts.managers.render_to_string')
    @patch('accounts.managers.UserManager._create_temporary_link')
    def test_send_user_activation_email(self, mock_link, mock_render, mailoutbox):
        user = mixer.blend(User, is_active=False)
        mock_link.return_value = 'https://fakelink'
        User.objects.send_activation_email(user=user)

        args, _ = mock_render.call_args_list[0]
        assert args[0] == 'activation_email.html'
        assert args[1].get('user') == user
        assert args[1].get('activation_link') == 'https://fakelink'

        assert len(mailoutbox) == 1
        email = mailoutbox[0]

        assert "Activate your account" == email.subject
        assert email.to == [user.email]

    def test_send_password_reset_email_invalid_config(self, settings):
        user = mixer.blend(User, is_active=True)
        settings.USER_PASSWORD_RESET_URI = None
        with pytest.raises(ImproperlyConfigured) as error:
            User.objects.send_password_reset_email(user=user)
            assert error.message == "No reset password URI specified."

    @patch('accounts.managers.render_to_string')
    @patch('accounts.managers.UserManager._create_temporary_link')
    def test_send_password_reset_email(self, mock_link, mock_render, mailoutbox):
        user = mixer.blend(User, is_active=True)
        mock_link.return_value = 'https://fakelink'
        User.objects.send_password_reset_email(user=user)

        args, _ = mock_render.call_args_list[0]
        assert args[0] == 'password_reset_email.html'
        assert args[1].get('user') == user
        assert args[1].get('password_reset_link') == 'https://fakelink'

        assert len(mailoutbox) == 1
        email = mailoutbox[0]

        assert "Reset your password" == email.subject
        assert email.to == [user.email]
