from django.db.models.fields import (
    DateField,
    DateTimeField,
    DecimalField,
    TimeField,
    UUIDField,
)
from django.db.models.fields.files import ImageField
from django.db.models.fields.related import ManyToManyField, RelatedField


def to_dict(instance, exclude=None):
    """
    Returns a dict containing the data in ``instance`` suitable for
    converting to JSON.

    ``exclude`` is an optional list of field names. If provided, the named
    fields will be excluded from the returned dict
    """

    data = {}
    opts = instance._meta

    for f in opts.concrete_fields + opts.many_to_many:
        if exclude and f.name in exclude:
            continue
        value = getattr(instance, f.name)
        if value:
            if isinstance(f, ManyToManyField):
                value = [
                    str(obj.pk) for obj in f.value_from_object(instance)
                ]
            elif isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(f, DateField):
                value = value.strftime('%Y-%m-%d')
            elif isinstance(f, TimeField):
                value = value.strftime('%H:%M:%S')
            elif isinstance(f, ImageField):
                value = value.url
            elif isinstance(f, DecimalField):
                value = round(float(value), f.decimal_places)
            elif isinstance(f, UUIDField) or isinstance(f, RelatedField):
                value = str(f.value_from_object(instance))
            else:
                value = f.value_from_object(instance)
        data[f.name] = value
    return data
