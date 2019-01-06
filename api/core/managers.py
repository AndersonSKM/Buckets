from django.db.models import Manager


class AbstractBaseManager(Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class BaseManager(AbstractBaseManager):
    pass
