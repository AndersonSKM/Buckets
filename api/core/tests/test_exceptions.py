from django.core.exceptions import ValidationError as DjangoValidationError
from mock import Mock
from rest_framework import status

from core.exceptions import exception_handler


class TestExceptionHandler:
    def test_django_exception_with_single_message(self):
        error = DjangoValidationError("Invalid combination")
        response = exception_handler(error, Mock())

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['non_field_errors'] == ["Invalid combination"]

    def test_django_exception_with_multiple_messages(self):
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

    def test_return_internal_server_error_with_standard_exception(self):
        error = Exception("Shit happens")
        response = exception_handler(error, Mock())

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert response.data['detail'] == str(error)
