from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

from accounts.models import User
from accounts.utils import decode_user_uuid, encode_user_uuid, user_activation_token


def create_temporary_link(user, token_generator, setting_name, error_msg):
    uuidb64 = encode_user_uuid(user.pk)
    token = token_generator.make_token(user)
    uri = getattr(settings, setting_name, None)
    if not uri:
        raise ImproperlyConfigured(error_msg)
    return uri.format(uuidb64=uuidb64, token=token)


def user_activation_link(user):
    return create_temporary_link(
        user=user,
        token_generator=user_activation_token,
        setting_name='USER_ACTIVATION_URI',
        error_msg="No activation URI specified."
    )


def user_password_reset_link(user):
    return create_temporary_link(
        user=user,
        token_generator=default_token_generator,
        setting_name='USER_PASSWORD_RESET_URI',
        error_msg="No reset password URI specified."
    )


def user_from_uuidb64(uuidb64):
    try:
        uuid = decode_user_uuid(uuidb64)
        return User.objects.get(pk=uuid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def send_user_activation_email(user):
    if user.is_active:
        raise ValidationError("User already active.")
    message = render_to_string('activation_email.html', {
        'user': user,
        'activation_link': user_activation_link(user)
    })
    user.email_user("Activate your account", message, fail_silently=False)


def send_user_password_reset_email(user):
    if not user.is_active:
        raise ValidationError("User isn't already active.")
    message = render_to_string('password_reset_email.html', {
        'user': user,
        'password_reset_link': user_password_reset_link(user)
    })
    user.email_user("Reset your password", message, fail_silently=False)
