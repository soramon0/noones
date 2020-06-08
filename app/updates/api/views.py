from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings

from updates.models import MeasuresUpdate, PhotosUpdate
from models.models import Mensuration
from updates.api.serializers import (
    MeasuresUpdateSerializer,
    PhotosUpdateSerializer,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_measures_update(request):
    serializer = MeasuresUpdateSerializer(data=request.data)
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


class MeasuresUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            measure = Mensuration.objects.get(pk=pk)
            return measure.measuresupdate
        except MeasuresUpdate.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        measures_update = self.get_object(pk=pk)
        serializer = MeasuresUpdateSerializer(measures_update)
        return Response(serializer.data)

    def put(self, request, pk):
        measures_update = self.get_object(pk=pk)

        if measures_update.accept:
            # this update has already been accepted and will be deleted
            # in the next 24h so the user should not be able to change it
            res = {
                "measure": ["this update has already been accepted and will be deleted in the next 24h."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        serializer = MeasuresUpdateSerializer(
            measures_update, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        measures_update = self.get_object(pk=pk)
        measures_update.delete()

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
def create_gallery(request):
    try:
        images = request.data.getlist('image')
    except AttributeError:
        return Response({'image': ['No file was submitted.']}, status=status.HTTP_400_BAD_REQUEST)

    # The uploaded images will belong to the current logged in user
    data = {'model': request.user.model.id}

    # A list to keep track of all uploaded images
    uploaded_images = []

    # the user shouldn't be able to upload more than 8 images
    # get the count of images in the database and check that the user
    # hasn't upload more than 8
    gallery_count = PhotosUpdate.objects.filter(model=data['model']).count()
    max_upload_count = 8
    images_to_upload = len(images)

    if (gallery_count + images_to_upload) > max_upload_count:
        # TODO(karim): maybe handle this on the client
        # and return here just the uploaded pictures
        res = {'image': [
            f"You can only upload {max_upload_count} photos; you've uploaded {gallery_count} so far."]}
        return Response(res, status=status.HTTP_400_BAD_REQUEST)

    for image in images:
        # add image field to fulfill the needs
        # of the photos_update table
        data['image'] = image
        serializer = PhotosUpdateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        uploaded_images.append(serializer.data)

    return Response(uploaded_images, status=status.HTTP_201_CREATED)
