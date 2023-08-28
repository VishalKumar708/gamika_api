
from rest_framework.generics import *
from .serializers import PartialCitySerializer, CitySerializer, GetAllAreaByCitySerializer, GetAllBusinessByCitySerializer
from rest_framework import status
from rest_framework.response import Response
from .models import City, Business

from rest_framework.exceptions import ValidationError
from django.http import Http404


class GetAllApprovedCity(ListAPIView):
    queryset = City.objects.all().order_by('cityName')
    serializer_class = PartialCitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=True, isVerified=True))
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data as needed
        if len(serializer.data) == 0:
            data = {'msg': '0 approved cities are available.'}
        else:
            data = serializer.data
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetAllUnapprovedCityLAV(ListAPIView):
    queryset = City.objects.all()
    serializer_class = PartialCitySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=False, isVerified=False)).order_by('cityName')
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) == 0:
            data = {'msg': '0 unapproved cities are available.'}
        else:
            data = serializer.data
        # Customize the response data as needed
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetCityById(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'cityId'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Http404,ValidationError):
            msg = {'msg': 'No match Found.Please input valid cityId.'}
            json_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': msg
            }
            return Response(json_data)

        serializer = self.get_serializer(instance)
        json_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': serializer.data,
        }
        return Response(json_data)


# Get all areas by cityId
class GetAreaByCityId(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = GetAllAreaByCitySerializer
    lookup_field = 'cityId'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Http404, ValidationError):
            msg = {'msg': 'No match Found.Please input valid cityId.'}
            json_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': msg
            }
            return Response(json_data)

        serializer = self.get_serializer(instance)
        json_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': serializer.data,
        }

        return Response(json_data)


# get all business by city id
class GetAllBusinessByCityId(RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = GetAllBusinessByCitySerializer
    lookup_field = 'cityId'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Http404, ValidationError):
            msg = {'msg': 'No match Found.Please input valid cityId.'}
            json_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': msg
            }
            return Response(json_data)


        serializer = self.get_serializer(instance)
        json_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': serializer.data,
        }

        return Response(json_data)


class CreateNewCity(CreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def create(self, request, *args, **kwargs):
        try:
            # check city already exist or not
            city_name = request.data.get('cityName')
            matching_cities_count = City.objects.filter(cityName__iexact=city_name).count()
            if matching_cities_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{city_name}' already exists."},
                }
                return Response(json_data, status=302)

            # chekc city,state are not None and description is None
            city = request.data.get('cityName')
            state_name = request.data.get('state')
            description = request.data.get('description', None)
            data = request.data
            # Add data in description field
            if city is not None and state_name is not None and description is None:
                modify_data = request.data.copy()
                modify_data['description'] = city+state_name
                data = modify_data

            # Deserialize the request data and validate it using the serializer
            serializer = self.get_serializer(data=data)
            # check validation
            serializer.is_valid(raise_exception=True)

            # Save the new city object
            self.perform_create(serializer)

            # Customize the success response data
            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'status': 'Created',
                'message': 'City created successfully.',
            }
            # headers = self.get_success_headers(serializer.data)
            # return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)
            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Handle the case when request data is not valid
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'error',
                'errors': e.detail,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class UpdateCityById(UpdateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'cityId'

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # check user provide value or not
            if len(request.data) < 1:
                serializer = self.get_serializer(instance, data=request.data)
                serializer.is_valid(raise_exception=True)
                response_data = {
                    'status_code': status.HTTP_204_NO_CONTENT,
                    'status': 'failed',
                    'message': serializer.errors,
                }
                return Response(response_data, status=status.HTTP_204_NO_CONTENT)
            # check updated city is available or not
            city_name = request.data.get('cityName')
            matching_cities_count = City.objects.filter(cityName__iexact=city_name).count()
            if matching_cities_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{city_name}' already exists."},
                }
                return Response(json_data)

            # if city is not available then update it.
            # Deserialize the request data and validate it using the serializer
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Save the updated city object
            self.perform_update(serializer)

            # Customize the response data if needed
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'message': 'City updated successfully.',
                'data': serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except ValidationError as e:

            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'error',
                'errors': e.detail,
            }
            return Response(response_data)
        # if id is not found
        except Http404:
            msg = {'msg': 'No match Found.Please input valid cityId.'}
            json_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': msg
            }
            return Response(json_data)
