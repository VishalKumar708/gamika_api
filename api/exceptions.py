# myapp/exceptions.py
from rest_framework.exceptions import APIException


class MyCustomException(APIException):
    status_code = 500
    default_detail = 'Something went wrong.'
    default_code = 'server_error'
