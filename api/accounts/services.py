from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

from accounts.models import User
from accounts.utils import decode_user_uuid, encode_user_uuid, user_activation_token


def user_activation_link(user, request=None):
    uuidb64 = encode_user_uuid(user.pk)
    token = user_activation_token.make_token(user)
    if not settings.USER_ACTIVATION_URI:
        raise ImproperlyConfigured("No activation URI specified.")
    return settings.USER_ACTIVATION_URI.format(uuidb64=uuidb64, token=token)


def user_from_uuidb64(uuidb64):
    try:
        uuid = decode_user_uuid(uuidb64)
        return User.objects.get(pk=uuid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def send_user_activation_email(user):
    if user.is_active:
        raise ValueError("User already active.")
    message = render_to_string('activation_email.html', {
        'user': user,
        'activation_link': user_activation_link(user)
    })
    user.email_user("Activate your account", message, fail_silently=False)
