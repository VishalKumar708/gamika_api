from rest_framework.generics import *
from .serializers import AartiSerializer, PartialAartiSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import Aarti

from django.db.models import Q
from rest_framework.exceptions import ValidationError
from django.http import Http404


class GetAllApprovedAarti(ListAPIView):
    queryset = Aarti.objects.all().order_by('aartiName')
    serializer_class = PartialAartiSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=True, isVerified=True))
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data as needed
        if len(serializer.data) == 0:
            data = {'msg': 'No Aarti found.'}
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


class GetAllUnapprovedAarti(ListAPIView):
    queryset = Aarti.objects.all().order_by('aartiName')
    serializer_class = PartialAartiSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=False, isVerified=False)).order_by('aartiName')
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) == 0:
            data = {'msg': 'No Aarti available.'}
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


class GetAartiById(RetrieveAPIView):
    serializer_class = AartiSerializer
    lookup_field = 'aartiId'

    def get_queryset(self):
        return Aarti.objects.all()

    def retrieve(self, request, *args, **kwargs):
        try:
            print(self.get_queryset())
            instance = self.get_object()

        except (Http404, ValidationError):

            msg = {'msg': 'No match Found.Please input valid AartiId.'}
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


class CreateNewAarti(CreateAPIView):
    serializer_class = AartiSerializer

    def get_queryset(self):
        return Aarti.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            # check AartiName is already exist or not
            name = request.data.get('aartiName')

            queryset_count = self.get_queryset().filter(aartiName__iexact=name).count()

            if queryset_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"{name} Aarti is already exists."},
                }
                return Response(json_data, status=302)

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
                'message': 'Aarti created successfully.',
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


class UpdateAartiById(UpdateAPIView):
    serializer_class = AartiSerializer
    lookup_field = 'aartiId'

    def get_queryset(self):
        return Aarti.objects.all()

    def update(self, request, *args, **kwargs):
        try:
            print('query_ser', self.queryset)
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

            # check updated AartiName is available or not
            aarti_id = kwargs['aartiId']
            name = request.data.get('aartiName')
            queryset_count = self.get_queryset().filter(Q(aartiName__iexact=name) & ~Q(aartiId=aarti_id)).count()
            if queryset_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"{name} Aarti is already exists."},
                }
                return Response(json_data, status=302)

            # if Literature is not available then update it.
            # Deserialize the request data and validate it using the serializer
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            # Save the updated city object
            self.perform_update(serializer)

            # Customize the response data if needed
            response_data = {
                'status_code': status.HTTP_200_OK,
                'status': 'Success',
                'message': 'Aarti updated successfully.',
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
            msg = {'msg': 'No match Found.Please input valid AartiId.'}
            json_data = {
                'status_code': status.HTTP_404_NOT_FOUND,
                'status': 'error',
                'data': msg
            }
            return Response(json_data)
