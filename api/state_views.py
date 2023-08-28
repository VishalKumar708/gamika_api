
from rest_framework.generics import *
from .serializers import *
from rest_framework import status
from rest_framework.response import Response

from rest_framework.exceptions import ValidationError
from django.http import Http404
from .models import State


class GetAllApprovedState(ListAPIView):
    queryset = State.objects.all().order_by('stateName')
    serializer_class = PartialStateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=True, isVerified=True))
        serializer = self.get_serializer(queryset, many=True)

        # Customize the response data as needed
        if len(serializer.data) == 0:
            data = {'msg': 'No state found.'}
        else:
            data = serializer.data
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetAllUnapprovedState(ListAPIView):
    queryset = State.objects.all()
    serializer_class = PartialStateSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset().filter(isActive=False, isVerified=False)).order_by('stateName')
        serializer = self.get_serializer(queryset, many=True)
        if len(serializer.data) == 0:
            data = {'msg': '0 unapproved states are available.'}
        else:
            data = serializer.data
        # Customize the response data as needed
        response_data = {
            'status_code': status.HTTP_200_OK,
            'status': 'Success',
            'data': data,
        }

        return Response(response_data)


class GetStateById(RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = PartialStateSerializer
    lookup_field = 'stateId'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Http404, ValidationError):
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


class GetCitiesByStateId(RetrieveAPIView):
    queryset = State.objects.all()
    serializer_class = GetAllCitiesByStateSerializer
    lookup_field = 'stateId'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except (Http404, ValidationError):
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


class CreateNewState(CreateAPIView):
    queryset = City.objects.all()
    serializer_class = StateSerializer

    def create(self, request, *args, **kwargs):
        try:
            # check city already exist or not
            state_name = request.data.get('stateName')
            matching_state_count = State.objects.filter(stateName__iexact=state_name).count()
            if matching_state_count > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{state_name}' is already exists."},
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
                'message': 'State created successfully.',
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


class UpdateStateById(UpdateAPIView):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    lookup_field = 'stateId'

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

            # check updated state is available or not
            state_name = request.data.get('stateName')
            matching_state_counts = State.objects.filter(stateName__iexact=state_name).count()
            print(matching_state_counts)
            if matching_state_counts > 0:
                json_data = {
                    'status_code': status.HTTP_302_FOUND,
                    'status': 'failed',
                    'message': {'msg': f"'{state_name}' is already exists."},
                }
                return Response(json_data, status=status.HTTP_302_FOUND)

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
                'message': 'State updated successfully.',
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
