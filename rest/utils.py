from rest_framework.views import exception_handler


def custom_exception_handler(exc, content):
    response = exception_handler(exc, content)
    if response is not None:
        response.data['status'] = response.status_code
    return response
