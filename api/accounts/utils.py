from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_user_uuid(uuid):
    return urlsafe_base64_encode(force_bytes(uuid)).decode()


def decode_user_uuid(uuid):
    return force_text(urlsafe_base64_decode(uuid))


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


user_activation_token = UserActivationTokenGenerator()
