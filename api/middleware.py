import logging

from django.http import JsonResponse
from rest_framework import status

from rest_framework.response import Response
from .exceptions import MyCustomException

class Json404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            print('#################################')
            response = self.get_response(request)
            print('*************************************')

            if response.status_code == 404:
                response_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'status': 'failed',
                    'msg': 'Please provide a valid URL',
                }
                return JsonResponse(response_data, status=404)
            print("##################exception occur**************")
            return response
        except Exception as e:
            print("##################exception occur**************", e)
            response = self.process_exception(request, e)
            return response

    def process_exception(self, request, exception):
        error_message = str(exception)
        status_code = 500
        error_response = {
            'error': error_message,
            'status_code': status_code,
            'status': 'failed'
        }
        return JsonResponse(error_response, status=status_code)


