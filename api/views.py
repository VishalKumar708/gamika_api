
from .serializers import CitySerializer
from rest_framework.views import APIView
import io

from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import *
from rest_framework import status
from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404
method_decorator(csrf_exempt, name='dispatch')

class CityCURD(APIView):

    def get_object_by_id(self, id):
        try:
            city_obj = City.objects.get(cityId=id)
        except City.DoesNotExist:
            city_obj = None
        return city_obj

    def get(self,request,*args,**kwargs):


        try:
            id = request.GET.get('id',None)

            if id is None:
                city_status = request.GET.get('city_status')

                qs = City.objects.all()
                if city_status == 'approved':
                    qs = qs.filter(Q(isVerified='True') & Q(isActive='True'))

                elif city_status == 'unapproved':
                    qs = qs.filter(Q(isVerified='False') | Q(isActive='False'))
                elif city_status or city_status == '':
                    msg = {'msg':'Please provide valid value of status "approved/unapproved"'}
                    json_data = {
                        'status_code': status.HTTP_404_NOT_FOUND,
                        'status': 'failed',
                        'data': msg
                    }
                    return Response(json_data,status=404)
                serializer = CitySerializer(qs,many=True)
                json_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'success',
                    'data': serializer.data
                }

                return Response(json_data)

            obj = self.get_object_by_id(id)

            if obj is None:
                msg = {'msg': 'No match found'}
                json_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'status': 'failed',
                    'data': msg
                }
                return Response(json_data,status=404)

            serializer = CitySerializer(obj)
            json_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'success',
                'data': serializer.data
            }
            return Response(json_data)
        except Exception as e:
            json_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': str(e)
            }
            return Response(json_data, status=500)

    def put(self, request, format=None):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            data = JSONParser().parse(stream)
            cityId = data.get('cityId',None)
            if cityId is None:
                json_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'status': 'error',
                    'data': 'Please provide id to update the resource.'
                }
                return Response(json_data,status=404)
            obj = City.objects.get(cityId=cityId)
            serializer = CitySerializer(obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                msg = {'msg':'Resource Update Successfully.'}
                json_data = {
                    'status_code': status.HTTP_201_CREATED,
                    'status': 'success',
                    'data': msg
                }
                return Response(json_data)
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'error',
                'data': serializer.errors
            }

            return Response(json_data,status=406)
        except Exception as e:
            json_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': str(e)
            }
            return Response(json_data, status=500)

    def patch(self, request, format=None):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            data = JSONParser().parse(stream)
            cityId = data.get('cityId',None)
            if cityId is None:
                json_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'status': 'error',
                    'data': 'Please provide id to update the resource.'
                }
                return Response(json_data,status=404)
            obj = City.objects.get(cityId=cityId)
            serializer = CitySerializer(obj,data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                msg = {'msg':'Resource Update Successfully.'}
                json_data = {
                    'status_code': status.HTTP_201_CREATED,
                    'status': 'success',
                    'data': msg
                }
                return Response(json_data)
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'error',
                'data': serializer.errors
            }

            return Response(json_data,status=406)
        except Exception as e:
            json_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': str(e)
            }
            return Response(json_data, status=500)

    def post(self,request,*args,**kwargs):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            pdata = JSONParser().parse(stream)
            serializer = CitySerializer(data=pdata)
            if serializer.is_valid():
                serializer.save()
                res = {'msg': 'City created successfully!!'}
                json_data = {
                    'status_code': status.HTTP_200_OK,
                    'status': 'success',
                    'data': res
                }
                return Response(json_data)
            json_data = {
                'status_code': status.HTTP_406_NOT_ACCEPTABLE,
                'status': 'error',
                'data': serializer.errors
            }
            return Response(json_data, status=406)
        except Exception as e:
            json_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': str(e)
            }
            return Response(json_data, status=500)
# Create your views here.
    def delete(self, request, format=None):
        try:
            json_data = request.body
            stream = io.BytesIO(json_data)
            data = JSONParser().parse(stream)
            cityId = data.get('cityId',None)
            obj = self.get_object_by_id(cityId)
            if obj is None:
                msg = {'msg':'Resource not found.Please provide valid id to delete Resource.'}
                json_data = {
                    'status_code': status.HTTP_404_NOT_FOUND,
                    'status': 'failed',
                    'data': msg
                }
                return Response(json_data,status=404)

            obj.delete()
            msg = {'msg': 'Resource deleted successfully.'}
            json_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'success',
                'data': msg
            }
            return Response(json_data)

        except Exception as e:
            json_data = {
                'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                'status': 'error',
                'data': str(e)
            }
            return Response(json_data, status=500)


def custom_404_view(request, exception):
    response_data = {
        'status_code': status.HTTP_404_NOT_FOUND,
        'status': 'failed',
        'msg': 'Please provide a valid URL',
    }
    return Response(response_data, status=404)



def my_api_view(request):
    # Example: Try to access a non-existent dictionary key
    # data = {}
    # value = data['non_existent_key']
    # return Response({"result": value})
    return Response({"result": "success"})