import json
import uuid

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.indexes import GinIndex
from django.core import serializers
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _

from core.managers import AbstractBaseManager, BaseManager
from core.utils.fields import ChoiceEnum

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


class DBActions(ChoiceEnum):
    CREATE = 'Create'
    UPDATE = 'Update'
    DESTROY = 'Destroy'


class Revision(UUIDModelMixin, TimeStampModelMixin):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    action = models.CharField(max_length=25, choices=DBActions.choices(), editable=False)
    data = JSONField(editable=False)

    class Meta:
        ordering = ['-created_at',]
        db_table = 'revision'
        verbose_name = _('revision')
        verbose_name_plural = _('revisions')
        indexes = [
            models.Index(fields=['content_type',]),
            GinIndex(fields=['data',]),
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        if instance:
            kwargs['content_type_id'] = self._instance_content_type(instance)
            kwargs['action'] = self._instance_action(instance)
            kwargs['data'] = self._serialize_instance(instance)
        super(Revision, self).__init__(*args, **kwargs)

    @staticmethod
    def _serialize_instance(instance):
        data = serializers.serialize('json', [instance,])
        return json.loads(data)[0]

    @staticmethod
    def _instance_action(instance):
        if instance._state.adding:
            return DBActions.CREATE
        elif getattr(instance._state, 'destroing', False):
            return DBActions.DESTROY
        return DBActions.UPDATE

    @staticmethod
    def _instance_content_type(instance):
        return ContentType.objects.get_for_model(instance).pk


class RevisionModelMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        with transaction.atomic():
            Revision.objects.create(instance=self)
            super(RevisionModelMixin, self).save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields
            )

    def delete(self, using=None, keep_parents=False):
        self._state.destroing = True
        with transaction.atomic():
            Revision.objects.create(instance=self)
            super(RevisionModelMixin, self).delete(
                using=using,
                keep_parents=keep_parents
            )


# Base Models


class AbstractBaseModel(UUIDModelMixin, TimeStampModelMixin, RevisionModelMixin):
    objects = AbstractBaseManager()

    class Meta:
        abstract = True


class BaseModel(AbstractBaseModel, UserModelMixin):
    objects = BaseManager()

    class Meta:
        abstract = True
