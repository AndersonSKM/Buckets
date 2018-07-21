from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.managers import AbstractBaseManager
from core.models import AbstractBaseModel


class UserManager(BaseUserManager, AbstractBaseManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, is_active, **kwargs):
        if not email:
            raise ValueError(_("Users must have an email address"))

        user = self.model(
            email=self.normalize_email(email),
            is_staff=is_staff,
            is_active=is_active,
            is_superuser=is_superuser,
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, is_staff=False, **kwargs):
        return self._create_user(email, password, is_staff, False, False, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        return self._create_user(email, password, True, True, True, **kwargs)


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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.is_superuser and not self.is_staff:
            self.is_staff = True
        super(User, self).save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields
        )

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def activate(self):
        if self.is_active:
            return
        self.is_active = True
        self.save()
