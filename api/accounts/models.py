from typing import Any, List, Optional

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import AbstractBaseManager
from core.models import AbstractBaseModel


class UserManager(BaseUserManager, AbstractBaseManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str, is_staff: bool,
                     is_superuser: bool, is_active: bool, **extra_fields: dict) -> models.Model:
        if not email:
            raise ValueError(_("Users must have an email address"))

        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, is_staff: bool = False,
                    **extra_fields: dict) -> models.Model:
        return self._create_user(email, password, is_staff, False, False, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields: dict) -> models.Model:
        return self._create_user(email, password, True, True, True, **extra_fields)


class User(AbstractBaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=False)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self) -> str:
        return self.email

    def save(self, force_insert: bool = False, force_update: bool = False,
             using: Optional[str] = None, update_fields: Optional[List[str]] = None) -> None:
        if self.is_superuser and not self.is_staff:
            self.is_staff = True
        super(User, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def get_full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self) -> str:
        return self.first_name

    def email_user(self, subject: str, message: str, from_email: Optional[str] = None,
                   **kwargs: Any) -> None:
        send_mail(subject, message, from_email, [self.email], **kwargs)
