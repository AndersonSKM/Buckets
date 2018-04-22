from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.querysets import BaseQuerySet


class RevisionsManagerMixin(models.Manager):
    def get_revisions(self, pk):
        from .models import Revision

        content_type = ContentType.objects.get_for_model(self.model)
        return Revision.objects.filter(
            content_type__id=content_type.pk,
            object_pk=pk
        )


class AbstractBaseManager(RevisionsManagerMixin, models.Manager):
    _queryset_class = BaseQuerySet

    def get_queryset(self, *args, **kwargs):
        if kwargs.get('deleted', False):
            return self._queryset_class(self.model, using=self._db)
        return self._queryset_class(self.model, using=self._db).active()

    def full(self):
        return self.get_queryset(deleted=True)


class BaseManager(AbstractBaseManager):
    def from_user(self, email):
        return self.get_queryset().filter(user=email)
