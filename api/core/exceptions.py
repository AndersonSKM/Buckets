from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.views import exception_handler as drf_exception_handler


def exception_handler(exception, context):
    if isinstance(exception, DjangoValidationError):
        message = getattr(exception, 'message', None)
        messages = getattr(exception, 'messages', None)
        detail = {
            'non_field_errors': [message] or messages
        }
        exception = DRFValidationError(detail=detail)

    response = drf_exception_handler(exception, context)
    if response is None:
        exception = APIException(exception)
        return drf_exception_handler(exception, context)

    return response
