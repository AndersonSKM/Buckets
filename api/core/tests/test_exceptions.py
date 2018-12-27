from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import APIException
from rest_framework import status
from mock import Mock

from core.exceptions import exception_handler


class TestExceptionHandler:
    def test_django_exception_with_message(self):
        error = DjangoValidationError("Invalid combination")
        response = exception_handler(error, Mock())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Invalid combination"]

    def test_django_exception_with_message(self):
        error = DjangoValidationError([
            DjangoValidationError("Some invalid data"),
            DjangoValidationError("Another invalid field"),
        ])
        response = exception_handler(error, Mock())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == [
            "Some invalid data",
            "Another invalid field",
        ]
