from drf_standardized_errors.formatter import ExceptionFormatter
from drf_standardized_errors.types import ErrorResponse

from rest_framework import status


class CustomExceptionFormatter(ExceptionFormatter):
    def format_error_response(self, error_response: ErrorResponse):
        error = error_response.errors[0]
        return {
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": error.detail,
        }
