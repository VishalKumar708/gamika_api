from rest_framework.generics import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404
from .models import Area


class GetAllApprovedAreas(ListAPIView):
    queryset = Area.objects.all().order_by('areaName')
    serializer_class = PartialAreaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=True, isVerified=True))
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data as needed
        if len(serializer.data) == 0:
            data = {'msg': 'No Area found.'}
        else:
            data = serializer.data
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetAllUnapprovedAreas(ListAPIView):
    queryset = Area.objects.all().order_by('areaName')
    serializer_class = PartialAreaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=False, isVerified=False)).order_by('areaName')
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) == 0:
            data = {'msg': 'No Area available.'}
        else:
            data = serializer.data
        # Customize the response data as needed
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetAreaById(RetrieveAPIView):
    queryset = Area.objects.all()
    serializer_class = PartialAreaSerializer
    lookup_field = 'areaId'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Http404,ValidationError):
            msg = {'msg': 'No match Found.Please input valid stateId.'}
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


class CreateNewArea(CreateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

    def create(self, request, *args, **kwargs):
        try:
            # check city already exist or not
            area_name = request.data.get('areaName')
            city_id = request.data.get('cityId')
            queryset_count = self.get_queryset().filter(Q(cityId=city_id) & Q(areaName__iexact=area_name)).count()

            # matching_state_count = Area.objects.filter(areaName__iexact=area_name).count()
            if queryset_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"{area_name} area is already exists."},
                }
                return Response(json_data, status=302)

            # Deserialize the request data and validate it using the serializer
            serializer = self.get_serializer(data=request.data)
            # check validation
            serializer.is_valid(raise_exception=True)

            # Save the new city object
            self.perform_create(serializer)

            # Customize the success response data
            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'status': 'Created',
                'message': 'Area created successfully.',
            }
            return Response(response_data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            # Handle the case when request data is not valid
            response_data = {
                'status_code': status.HTTP_400_BAD_REQUEST,
                'status': 'error',
                'errors': e.detail,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class UpdateAreaById(UpdateAPIView):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    lookup_field = 'areaId'

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

            # check updated area is available or not
            area_name = request.data.get('areaName')
            city_id = request.data.get('cityId')
            queryset_count = self.get_queryset().filter(Q(cityId=city_id) & Q(areaName__iexact=area_name)).count()
            # if queryset_count is greater than 0 means area is available and show a failed message
            if queryset_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"{area_name} area is already exists."},
                }
                return Response(json_data, status=302)

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
                'message': 'Area updated successfully.',
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