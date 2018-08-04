from django.contrib.auth import password_validation as django_password_validation
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import exceptions as django_exceptions
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import serializers


def encode_user_uuid(uuid):
    return urlsafe_base64_encode(force_bytes(uuid)).decode()


def decode_user_uuid(uuid):
    return force_text(urlsafe_base64_decode(uuid))


def validate_password(password, user=None):
    try:
        django_password_validation.validate_password(password, user)
    except django_exceptions.ValidationError as error:
        raise serializers.ValidationError({'password': list(error.messages)})


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


user_activation_token = UserActivationTokenGenerator()
