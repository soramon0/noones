import os

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404

from accounts.api.permissions import IsOwner
from core.models import User
from models.models import Model, Mensuration, Photo
from .serializers import (
    ModelSerializer,
    UserSerializer,
    MeasuresSerializer,
    ProfilePictureSerializer,
    CoverPictureSerializer,
    PhotoSerializer
)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        user = request.user
        model = user.model
        user_serializer = UserSerializer(user)
        model_serializer = ModelSerializer(model)
        measures_serializer = MeasuresSerializer(model.measures)
        profileImage_serializer = ProfilePictureSerializer(model)
        coverImage_serializer = CoverPictureSerializer(model)

        # Get 8 user uploaded pictures that are in use
        # TODO(karim): change to inUse later
        photos = Photo.objects.filter(model=model, inUse=False)[:8]
        photo_serializer = PhotoSerializer(photos, many=True)

        res = {'model': model_serializer.data}
        res['model'].update({
            'email': user_serializer.data['email'],
            'profilePicture': profileImage_serializer.data['profilePicture'],
            'coverPicture': coverImage_serializer.data['coverPicture'],
        })
        res['measures'] = measures_serializer.data
        res['photos'] = photo_serializer.data

        return Response(res)

    except User.model.RelatedObjectDoesNotExist:
        # Handling when admin user logs in
        # admin does't have the requried fields for this page
        # So we redirect him
        # TODO(karim): handle the navigation to not include a link to this page
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ModelAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        model = self.get_object(pk=pk)
        serializer = ModelSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk):
        model = self.get_object(pk=pk)
        serializer = ModelSerializer(model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeasuresAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, pk):
        try:
            return Mensuration.objects.get(pk=pk)
        except Mensuration.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        measures = self.get_object(pk=pk)
        serializer = MeasuresSerializer(measures)
        return Response(serializer.data)

    def put(self, request, pk):
        measures = self.get_object(pk=pk)
        serializer = MeasuresSerializer(measures, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfilePictureAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, user):
        try:
            return Model.objects.filter(user=user).get()
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        model = self.get_object(user=request.user)
        serializer = ProfilePictureSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk=None):
        model = self.get_object(user=request.user) 
        serializer = ProfilePictureSerializer(model, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        PhotoSerializer.delete_old_image(model.profilePicture)
        # delete_old_image(model.profilePicture)

        # Save the new image
        serializer.save()
        return Response(serializer.data)


class CoverPictureAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self, user):
        try:
            return Model.objects.filter(user=user).get()
        except Model.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        model = self.get_object(user=request.user)
        serializer = CoverPictureSerializer(model)
        return Response(serializer.data)

    def put(self, request, pk=None):
        model = self.get_object(user=request.user)
        serializer = CoverPictureSerializer(model, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        PhotoSerializer.delete_old_image(model.coverPicture)

        # Save the new image
        serializer.save()
        return Response(serializer.data)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def gallery(request):
    model_id = request.user.model.id

    if request.method == 'GET':
        # TODO(karim): set inUse back to True
        photos = Photo.objects.filter(model=model_id, inUse=False)[:8]
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        try:
            images = request.data.getlist('image')
        except AttributeError:
            return Response({'image': ['No file was submitted']}, status=status.HTTP_400_BAD_REQUEST)

        # All the uploaded images will use the same model id
        data = {'model': model_id}
        # To keep track of all uploaded images
        uploaded_images = []

        # the user shouldn't be able to upload more than 8 images
        # get the count of images upoloaded and check that the user
        # hasn't upload more than 8
        gallery_count = Photo.objects.filter(model=model_id).count()
        max_upload_count = 8

        for image in images:
            if gallery_count < max_upload_count:
                data['image'] = image
                serializer = PhotoSerializer(data=data)
                if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                uploaded_images.append(serializer.data)
                gallery_count += 1
            else:
                # TODO(karim): maybe handle this on the client
                # and return here just the uploaded pictures
                res = {'image': [f"You can only upload {max_upload_count} photos; you've uploaded {gallery_count}"]}
                return Response(res, status=status.HTTP_400_BAD_REQUEST)

        return Response(uploaded_images, status=status.HTTP_201_CREATED)


class GalleryAPIView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]

    def put(self, request, pk):
        try:
            photo = Photo.objects.get(pk=pk)
        except Photo.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PhotoSerializer(photo, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        PhotoSerializer.delete_old_image(photo.image)

        # Save the new image
        serializer.save()
        return Response(serializer.data)