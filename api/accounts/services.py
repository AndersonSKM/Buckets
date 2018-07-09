from typing import Dict, Optional

from django.http import HttpRequest
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.reverse import reverse

from accounts.models import User
from accounts.utils import user_activation_token


class UserService:
    @staticmethod
    def activation_info(user: User, request: Optional[HttpRequest] = None) -> Dict[str, str]:
        uuid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = user_activation_token.make_token(user)
        uri = reverse(
            'auth:users-activate',
            args=[uuid, token],
            request=request
        )
        return {
            'user_full_name': user.get_full_name(),
            'uuid': uuid,
            'token': token,
            'uri': uri,
        }

    @staticmethod
    def user_from_uuidb64(uuidb64: str) -> User:
        try:
            uuid = force_text(urlsafe_base64_decode(uuidb64))
            user = User.objects.get(pk=uuid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        return user

    @staticmethod
    def activate(uuidb64: str, token: str) -> None:
        user = UserService.user_from_uuidb64(uuidb64)
        if user and user.is_active:
            return

        if not user_activation_token.check_token(user, token):
            raise ValueError("Invalid activation parameters")

        user.is_active = True
        user.save()

    @staticmethod
    def send_activation_email(user: User, request: Optional[HttpRequest] = None) -> None:
        if user.is_active:
            raise ValueError("User already active")
        info = UserService.activation_info(user, request)
        message = render_to_string('activation_email.html', info)
        user.email_user("Activate your account", message, fail_silently=False)
