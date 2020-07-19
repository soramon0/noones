from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from models.api.serializers import PhotoSerializer
from models.utils import delete_old_image

from models.models import Photo
from updates.models import (
    ModelUpdate,
    MeasuresUpdate,
    PhotosUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate
)
from updates.api.serializers import (
    ModelUpdateSerializer,
    MeasuresUpdateSerializer,
    PhotosUpdateSerializer,
    PhotosUpdateResterSerializer,
    ProfilePictureUpdateSerializer,
    CoverPictureUpdateSerializer
)

MAX_GALLERY_UPLOAD_COUNT = 8


class ModelUpdateViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk=None):
        try:
            return ModelUpdate.objects.filter(model=self.request.user.model.id).get()
        except ModelUpdate.DoesNotExist:
            raise Http404

    def list(self, request):
        instance = self.get_object()
        serializer = ModelUpdateSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data['model'] = request.user.model.id

        if ModelUpdate.objects.filter(model=data['model']).exists():
            context = {
                'model': ['do not create a new upadte request! Update the one you have.']
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = ModelUpdateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'Update Request from {request.user.email}',
            'New Update request for model',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()

        if instance.accept:
            # this update has already been accepted and will be deleted
            # in the next 24h so the user should not be able to change it
            context = {
                "model": ["this update has already been accepted and will be deleted in the next 24h."]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if not instance.decline:
            # Update permission is only allowed if it hasn't been 24 hours
            # but if the request was delined the user can update the request again
            now = timezone.now()
            upload_date = instance.created_at
            days = (now - upload_date).days

            if days != 0:
                context = {
                    "model": ["You can only update within the first 24 hours."]
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = ModelUpdateSerializer(instance, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.delete()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'User {request.user.email} deleted his update',
            'Delete request for measures update',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class MeasuresUpdateViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk=None):
        try:
            return MeasuresUpdate.objects.filter(measure=self.request.user.mensuration.id).get()
        except MeasuresUpdate.DoesNotExist:
            raise Http404

    def list(self, request):
        instance = self.get_object()
        serializer = MeasuresUpdateSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        data = request.data
        data['measure'] = request.user.mensuration.id

        if MeasuresUpdate.objects.filter(measure=data['measure']).exists():
            context = {
                'measure': ['do not create a new upadte request! Update the one you have.']
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = MeasuresUpdateSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'Update Request from {request.user.email}',
            'New Update request for measures',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = self.get_object()

        if instance.accept:
            # this update has already been accepted and will be deleted
            # in the next 24h so the user should not be able to change it
            context = {
                "measure": ["this update has already been accepted and will be deleted in the next 24h."]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        if not instance.decline:
            # Update permission is only allowed if it hasn't been 24 hours
            # but if the request was delined the user can update the request again
            now = timezone.now()
            upload_date = instance.created_at
            days = (now - upload_date).days

            if days != 0:
                context = {
                    "measure": ["You can only update within the first 24 hours."]
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

        serializer = MeasuresUpdateSerializer(instance, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        measures_update = self.get_object()
        measures_update.delete()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'User {request.user.email} deleted his update',
            'Delete request for measures update',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_gallery_update(request):
    model_id = request.user.model.id

    if request.method == 'GET':
        photos_update = PhotosUpdate.objects.filter(model=model_id)
        serializer = PhotosUpdateSerializer(photos_update, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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
        gallery_count = PhotosUpdate.objects.filter(
            model=data['model']).count()
        images_to_upload = len(images)

        if (gallery_count + images_to_upload) > MAX_GALLERY_UPLOAD_COUNT:
            # TODO(karim): maybe handle this on the client
            # and return here just the uploaded pictures
            res = {'image': [
                f"You can only upload {MAX_GALLERY_UPLOAD_COUNT} photos; you've uploaded {gallery_count} so far."]}
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


class GalleryUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return PhotosUpdate.objects.get(pk=pk, model=self.request.user.model.id)
        except PhotosUpdate.DoesNotExist:
            raise Http404

    def get(self, request, update_id):
        photo_update = self.get_object(pk=update_id)
        serializer = PhotosUpdateSerializer(photo_update)
        return Response(serializer.data)

    def put(self, request, update_id):
        photo_update = self.get_object(update_id)

        if photo_update.accept:
            # this update has already been accepted and will be deleted
            # in the next 24h so the user should not be able to change it
            res = {
                "image": ["this update has already been accepted and will be deleted in the next 24h."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if not photo_update.decline:
            # Update permission is only allowed if it hasn't been 24 hours
            # but if the request was delined the user can update the request again
            now = timezone.now()
            upload_date = photo_update.created_at
            days = (now - upload_date).days

            if days != 0:
                res = {
                    "image": ["You can only update within the first 24 hours."]
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # Only update the image field
        data = {
            'image': request.data.get('image'),
        }

        serializer = PhotosUpdateSerializer(
            photo_update, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        delete_old_image(photo_update.image)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, update_id):
        photo_update = self.get_object(pk=update_id)

        photo_update.delete()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'User {request.user.email} deleted his update',
            'Delete request for photo update',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_gallery(request, id):
    model_id = request.user.model.id

    # TODO(karim): improve this api call to modify an update if it exists
    # or create a new one
    data = {
        'image': request.data.get('image', None),
    }
    try:
        photo_update = PhotosUpdate.objects.filter(
            related_photo=id, model=model_id).get()

        # get a refrence to the old image to compare against later
        old_image = photo_update.image

        serializer = PhotosUpdateResterSerializer(
            photo_update, data=data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        # check that the old image is not refrenced anymore
        # by the update or the gallery
        if old_image.path != photo_update.related_photo.image.path and old_image.path != photo_update.image.path:
            delete_old_image(old_image)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except PhotosUpdate.DoesNotExist:
        if not Photo.objects.filter(pk=id, model=model_id).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)

        data['model'] = model_id
        data['related_photo'] = id

        serializer = PhotosUpdateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_profile_picture_update(request):
    model_id = request.user.model.id

    if request.method == 'GET':
        profile_update = ProfilePictureUpdate.objects.filter(model=model_id)
        serializer = ProfilePictureUpdateSerializer(profile_update, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'image': request.data.get('image', None), 'model': model_id}
        serializer = ProfilePictureUpdateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


class ProfilePictureUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProfilePictureUpdate.objects.get(pk=pk, model=self.request.user.model.id)
        except ProfilePictureUpdate.DoesNotExist:
            raise Http404

    def put(self, request, update_id):
        photo_update = self.get_object(update_id)

        if photo_update.accept:
            # this update has already been accepted and will be deleted
            # in the next 24h so the user should not be able to change it
            res = {
                "image": ["this update has already been accepted and will be deleted in the next 24h."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if not photo_update.decline:
            # Update permission is only allowed if it hasn't been 24 hours
            # but if the request was delined the user can update the request again
            now = timezone.now()
            upload_date = photo_update.created_at
            days = (now - upload_date).days

            if days != 0:
                res = {
                    "image": ["You can only update within the first 24 hours."]
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # Only update the image field
        data = {
            'image': request.data.get('image'),
        }

        serializer = ProfilePictureUpdateSerializer(
            photo_update, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        delete_old_image(photo_update.image)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, update_id):
        photo_update = self.get_object(pk=update_id)

        photo_update.delete()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'User {request.user.email} deleted his update',
            'Delete request for profile photo update',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_or_create_cover_picture_update(request):
    model_id = request.user.model.id

    if request.method == 'GET':
        profile_update = CoverPictureUpdate.objects.filter(model=model_id)
        serializer = CoverPictureUpdateSerializer(profile_update, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'image': request.data.get('image', None), 'model': model_id}
        serializer = CoverPictureUpdateSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)


class CoverPictureUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CoverPictureUpdate.objects.get(pk=pk, model=self.request.user.model.id)
        except CoverPictureUpdate.DoesNotExist:
            raise Http404

    def put(self, request, update_id):
        photo_update = self.get_object(update_id)

        if photo_update.accept:
            # this update has already been accepted and will be deleted
            # in the next 24h so the user should not be able to change it
            res = {
                "image": ["this update has already been accepted and will be deleted in the next 24h."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        if not photo_update.decline:
            # Update permission is only allowed if it hasn't been 24 hours
            # but if the request was delined the user can update the request again
            now = timezone.now()
            upload_date = photo_update.created_at
            days = (now - upload_date).days

            if days != 0:
                res = {
                    "image": ["You can only update within the first 24 hours."]
                }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        # Only update the image field
        data = {
            'image': request.data.get('image'),
        }

        serializer = CoverPictureUpdateSerializer(
            photo_update, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        delete_old_image(photo_update.image)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, update_id):
        photo_update = self.get_object(pk=update_id)

        photo_update.delete()

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f'User {request.user.email} deleted his update',
            'Delete request for cover photo update',
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
