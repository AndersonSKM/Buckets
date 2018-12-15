from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from accounts.utils import decode_user_uuid, encode_user_uuid, user_activation_token
from core.managers import AbstractBaseManager


class UserManager(BaseUserManager, AbstractBaseManager):
    use_in_migrations = True

    def create_user(self, email, password, confirm, is_staff=False, **kwargs):
        return self._create_user(email, password, confirm, is_staff, False, **kwargs)

    def create_superuser(self, email, password, confirm, **kwargs):
        return self._create_user(email, password, confirm, True, True, **kwargs)

    def change_current_password(self, user, current_password, password, confirm):
        if not user.check_password(current_password):
            raise ValidationError(_("Invalid current password."))
        self.update_password(user=user, password=password, confirm=confirm)

    def update_password(self, user, password, confirm, commit=True):
        if password != confirm:
            raise ValidationError(_("Passwords don't match."))

        validate_password(password, user=user)
        user.set_password(password)
        if commit:
            user.save(update_fields=['password'], using=self._db)

    def activate(self, user, commit=True):
        if user.is_active:
            return

        user.is_active = True
        if commit:
            user.save(update_fields=['is_active'], using=self._db)

    def send_activation_email(self, user):
        if user.is_active:
            raise ValidationError(_("User already active."))
        link = self._create_temporary_link(
            user=user,
            token_generator=user_activation_token,
            setting_name='USER_ACTIVATION_URI',
            error_msg=_("No activation URI specified.")
        )
        message = render_to_string('activation_email.html', {
            'user': user,
            'activation_link': link
        })
        self.email_user(
            user=user,
            subject=_("Activate your account"),
            message=message,
            fail_silently=False
        )

    def send_password_reset_email(self, user):
        link = self._create_temporary_link(
            user=user,
            token_generator=default_token_generator,
            setting_name='USER_PASSWORD_RESET_URI',
            error_msg=_("No reset password URI specified.")
        )
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'password_reset_link': link
        })
        self.email_user(
            user=user,
            subject=_("Reset your password"),
            message=message,
            fail_silently=False
        )

    @staticmethod
    def email_user(user, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [user.email], **kwargs)

    def get_active_users(self, **kwargs):
        kwargs['is_active'] = True
        return self.get_queryset().filter(**kwargs)

    def get_active_or_none(self, **kwargs):
        kwargs['is_active'] = True
        return self.get_or_none(**kwargs)

    def get_user_by_uuid_token(self, uuidb64, token, generator):
        user = self.get_user_from_uuidb64(uuidb64)
        if not user:
            raise ValidationError(_("Invalid user id or user doesn't exist."))
        if not generator.check_token(user, token):
            raise ValidationError(_("Invalid token for given user."))
        return user

    def get_user_from_uuidb64(self, uuidb64):
        try:
            uuid = decode_user_uuid(uuidb64)
            return self.get_or_none(pk=uuid)
        except (TypeError, ValueError, OverflowError):
            return None

    @transaction.atomic
    def _create_user(self, email, password, confirm, is_staff, is_superuser, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=False,
            **kwargs
        )

        if user.is_superuser or settings.DEBUG:
            self.activate(user=user, commit=False)

        self.update_password(user=user, password=password, confirm=confirm, commit=False)

        if not user.is_active:
            self.send_activation_email(user=user)

        user.save(using=self._db)
        return user

    @staticmethod
    def _create_temporary_link(user, token_generator, setting_name, error_msg):
        uuidb64 = encode_user_uuid(user.pk)
        token = token_generator.make_token(user)
        uri = getattr(settings, setting_name, None)
        if not uri:
            raise ImproperlyConfigured(error_msg)
        return uri.format(uuidb64=uuidb64, token=token)
