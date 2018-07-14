from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.reverse import reverse

from accounts.models import User
from accounts.utils import user_activation_token


def user_activation_info(user, request=None):
    uuid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
    token = user_activation_token.make_token(user)
    uri = reverse('auth:users-activate', args=[uuid, token,], request=request)
    return {
        'user_full_name': user.get_full_name(),
        'uuid': uuid,
        'token': token,
        'uri': uri,
    }


def user_from_uuidb64(uuidb64):
    try:
        uuid = force_text(urlsafe_base64_decode(uuidb64))
        user = User.objects.get(pk=uuid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return user


def activate_user(uuidb64, token):
    user = user_from_uuidb64(uuidb64)
    if not user or not user_activation_token.check_token(user, token):
        raise ValueError("Invalid activation parameters")
    if user.is_active:
        return

    user.is_active = True
    user.save()


def send_user_activation_email(user, request=None):
    if user.is_active:
        raise ValueError("User already active")
    info = user_activation_info(user, request)
    message = render_to_string('activation_email.html', info)
    user.email_user("Activate your account", message, fail_silently=False)
