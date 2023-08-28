from rest_framework.generics import *
from .serializers import AartiSerializer, PartialAartiSerializer, BusinessSerializer, PartialBusinessSerializer
from rest_framework import status
from rest_framework.response import Response

from .models import Business,Aarti

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404


class GetAllApprovedBusiness(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = PartialBusinessSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=True, isVerified=True))
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data as needed
        if len(serializer.data) == 0:
            data = {'msg': 'No Business found.'}
            status_code = status.HTTP_204_NO_CONTENT
        else:
            data = serializer.data
            status_code = status.HTTP_200_OK
        response_data = {
            'status_code': status_code,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetAllUnapprovedBusiness(ListAPIView):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=False, isVerified=False)).order_by('businessName')
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) == 0:
            data = {'msg': 'Business Not Found.'}
            status_code = status.HTTP_204_NO_CONTENT
        else:
            data = serializer.data
            status_code = status.HTTP_200_OK
        # Customize the response data as needed
        response_data = {
            'status_code': status_code,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetBusinessById(RetrieveAPIView):
    serializer_class = BusinessSerializer
    lookup_field = 'businessId'

    def get_queryset(self):
        return Business.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            print(self.get_queryset())
            instance = self.get_object()

        except (Http404, ValidationError):

            msg = {'msg': 'No match Found.Please input valid BusinessId.'}
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


class CreateNewBusiness(CreateAPIView):
    serializer_class = BusinessSerializer

    def get_queryset(self):
        return Business.objects.all()

    def create(self, request, *args, **kwargs):
        try:

            # Deserialize the request data and validate it using the serializer
            serializer = self.get_serializer(data=request.data)
            # check validation
            serializer.is_valid(raise_exception=True)

            # Save the new Aarti object
            self.perform_create(serializer)

            # Customize the success response data
            response_data = {
                'status_code': status.HTTP_201_CREATED,
                'status': 'Created',
                'message': 'Business created successfully.',
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


class UpdateBusinessById(UpdateAPIView):
    serializer_class = BusinessSerializer
    lookup_field = 'businessId'

    def get_queryset(self):
        return Business.objects.all()

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

            # Deserialize the request data and validate it using the serializer
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Save the updated city object
            self.perform_update(serializer)

            # Customize the response data if needed
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'message': 'Business updated successfully.',
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
            msg = {'msg': 'No match Found.Please input valid BusinessId.'}
            json_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': msg
            }
            return Response(json_data)

