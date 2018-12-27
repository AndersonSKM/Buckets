from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

from core.managers import AbstractBaseManager


class UserManager(BaseUserManager, AbstractBaseManager):
    use_in_migrations = True

    def create_user(self, email, password, ** kwargs):
        kwargs['is_staff'] = False
        kwargs['is_superuser'] = False
        return self._create_user(
            email=email,
            password=password,
            **kwargs
        )

    def create_superuser(self, email, password, **kwargs):
        kwargs['is_staff'] = True
        kwargs['is_superuser'] = True
        return self._create_user(
            email=email,
            password=password,
            **kwargs
        )

    def get_active_users(self, **kwargs):
        kwargs['is_active'] = True
        return self.get_queryset().filter(**kwargs)

    def get_active_or_none(self, **kwargs):
        kwargs['is_active'] = True
        return self.get_or_none(**kwargs)

    def _create_user(self, email, password, **kwargs):
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        user.is_active = kwargs.get('is_active', True)
        user.set_password(password)
        user.save(using=self._db)
        return user
