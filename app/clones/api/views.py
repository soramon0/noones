from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings

from clones.models import MeasuresClone
from models.models import Mensuration
from clones.api.serializers import (
    MeasuresCloneSerializer,
    PhotosCloneSerializer,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_measures_clone(request):
    serializer = MeasuresCloneSerializer(data=request.data)
    if not serializer.is_valid():
        if 'measure' in serializer.errors:
            # The user should be able to create only one update
            res = {'measure': [
                'do not create a new upadte request! Update the one you have.']}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()

    # Send Email to admin
    # TODO(karim): Update this email
    send_mail(
        f'Update Request from {request.user.email}',
        f'New Update request for measures',
        request.user.email,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

    return Response(serializer.data, status=status.HTTP_201_CREATED)


class MeasuresCloneAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            measure = Mensuration.objects.get(pk=pk)
            return measure.measuresclone
        except MeasuresClone.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        measures_clone = self.get_object(pk=pk)
        serializer = MeasuresCloneSerializer(measures_clone)
        return Response(serializer.data)

    def put(self, request, pk):
        measures_clone = self.get_object(pk=pk)
        serializer = MeasuresCloneSerializer(measures_clone, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        measures_clone = self.get_object(pk=pk)
        measures_clone.delete()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'User {request.user.email} deleted his update',
            f'Delete request for measures update',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_photo_clone(request):
    serializer = PhotosCloneSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
