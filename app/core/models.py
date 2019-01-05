import uuid

from django.conf import settings
from django.db import models, transaction

from core.managers import AbstractBaseManager, BaseManager

# Mixin's


class UUIDModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class UserModelMixin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, db_index=True)

    class Meta:
        abstract = True


class AbstractBaseModel(UUIDModelMixin, TimeStampModelMixin):
    objects = AbstractBaseManager()

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        with transaction.atomic():
            super().save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )


class BaseModel(AbstractBaseModel, UserModelMixin):
    objects = BaseManager()

    class Meta:
        abstract = True
