from datetime import datetime

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six

from accounts.models import User


class UserActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: datetime) -> str:
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)


user_activation_token = UserActivationTokenGenerator()
