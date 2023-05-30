from rest_framework.exceptions import APIException


class DBWriteError(APIException):
    status_code = 500
    default_detail = 'database_error'
    default_code = 'database_unavailable'
    