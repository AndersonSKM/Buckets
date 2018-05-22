from django.db import models
from django.utils import timezone


class SoftDeleteQuerySetMixin(models.QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySetMixin, self).update(
            deleted_at=timezone.now()
        )

    def undelete(self):
        return super(SoftDeleteQuerySetMixin, self).update(
            deleted_at=None
        )

    def destroy(self):
        return super(SoftDeleteQuerySetMixin, self).delete()

    def active(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.exclude(deleted_at__isnull=True)


class BaseQuerySet(SoftDeleteQuerySetMixin, models.QuerySet):
    pass
