import json
import uuid

from dirtyfields import DirtyFieldsMixin
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import FieldDoesNotExist
from django.db import models, transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.managers import AbstractBaseManager, BaseManager
from core.utils.fields import ChoiceEnum
from core.utils.models import to_dict

# Mixin's


class UUIDModelMixin(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True


class TimeStampModelMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModelMixin(models.Model):
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        editable=False
    )

    class Meta:
        abstract = True

    @transaction.atomic
    def destroy(self, *args, **kwargs):
        self._state.destroing = True
        Revision.objects.create(instance=self)
        super(SoftDeleteModelMixin, self).delete(*args, **kwargs)

    def delete(self):
        assert not self.deleted_at
        self.deleted_at = timezone.now()
        self.save()

    def undelete(self):
        assert self.deleted_at
        self.deleted_at = None
        self.save()


class UserModelMixin(models.Model):
    user = models.EmailField(
        editable=False,
        db_index=True
    )

    class Meta:
        abstract = True


class Revision(UUIDModelMixin, TimeStampModelMixin):
    class Actions(ChoiceEnum):
        CREATE = 'Create'
        UPDATE = 'Update'
        DELETE = 'Delete'
        UNDELETE = 'Undelete'
        DESTROY = 'Destroy'

    object_pk = models.UUIDField(
        editable=False
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    user = models.EmailField(
        editable=False,
        null=True,
        blank=True
    )
    action = models.CharField(
        max_length=25,
        choices=Actions.choices(),
        editable=False
    )
    serialized_data = models.TextField(
        editable=False
    )
    object = GenericForeignKey(
        ct_field='content_type',
        fk_field='object_pk',
    )

    class Meta:
        ordering = ['-created_at']
        db_table = 'revision'
        verbose_name = _('revision')
        verbose_name_plural = _('revisions')
        indexes = [
            models.Index(fields=['object_pk', 'content_type', 'user']),
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.pop('instance', None)
        if instance:
            kwargs['object_pk'] = instance.pk
            kwargs['content_type_id'] = instance.content_type_pk
            kwargs['serialized_data'] = self.serialize_instance(instance)
            kwargs['user'] = self._get_instance_user(instance)
            kwargs['action'] = self._get_instance_action(instance)
        super(Revision, self).__init__(*args, **kwargs)

    def serialize_instance(self, obj):
        return json.dumps(to_dict(obj))

    def json(self):
        return json.loads(self.serialized_data)

    def _get_instance_action(self, obj):
        if obj._state.adding:
            action = Revision.Actions.CREATE
        elif obj.is_deleting():
            action = Revision.Actions.DELETE
        elif obj.is_undeleting():
            action = Revision.Actions.UNDELETE
        elif getattr(obj._state, 'destroing', False):
            action = Revision.Actions.DESTROY
        else:
            action = Revision.Actions.UPDATE
        return action

    def _get_instance_user(self, obj):
        try:
            f = obj._meta.get_field('user')
        except FieldDoesNotExist:
            return None
        return obj.user if isinstance(f, models.EmailField) else None

# Base Classes


class AbstractBaseModel(
    UUIDModelMixin,
    TimeStampModelMixin,
    SoftDeleteModelMixin,
    DirtyFieldsMixin
):
    objects = AbstractBaseManager()

    class Meta:
        abstract = True

    @property
    def content_type_pk(self):
        return ContentType.objects.get_for_model(self).pk

    def save(self, *args, **kwargs):
        self.full_clean()
        self._execute_save(*args, **kwargs)

    def is_deleting(self):
        return 'deleted_at' in self.get_dirty_fields() and self.deleted_at

    def is_undeleting(self):
        return 'deleted_at' in self.get_dirty_fields() and not self.deleted_at

    @transaction.atomic
    def _execute_save(self, *args, **kwargs):
        Revision.objects.create(instance=self)
        super(AbstractBaseModel, self).save(*args, **kwargs)


class BaseModel(AbstractBaseModel, UserModelMixin):
    objects = BaseManager()

    class Meta:
        abstract = True
