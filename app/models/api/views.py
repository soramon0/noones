import os

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404

from core.models import User
from models.models import (
    Model,
    Mensuration,
    Photo,
    ProfilePicture,
    CoverPicture
)
from .serializers import (
    ModelSerializer,
    UserSerializer,
    MeasuresSerializer,
    ProfilePictureSerializer,
    CoverPictureSerializer,
    PhotoSerializer
)

from .pagination import CreatedAtPaginator


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    try:
        user = request.user
        model = user.model
        measures = user.mensuration
    except User.model.RelatedObjectDoesNotExist:
        # Handling when admin user logs in
        # admin does't have the requried fields for this page
        # So we redirect him
        # TODO(karim): handle the navigation to not include a link to this page
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    user_serializer = UserSerializer(user)
    model_serializer = ModelSerializer(model)
    measures_serializer = MeasuresSerializer(measures)

    # Gallery
    photos = Photo.objects.filter(model=model, inUse=True)[:8]
    photo_serializer = PhotoSerializer(photos, many=True)

    res = {
        'model': model_serializer.data,
        'measures': measures_serializer.data,
        'photos': photo_serializer.data
    }
    res['model'].update({'email': user_serializer.data['email']})

    try:
        profile_picture = ProfilePicture.objects.get(
            model=model.id, inUse=True)
        profile_picture_serializer = ProfilePictureSerializer(profile_picture)
        res['profilePicture'] = profile_picture_serializer.data
    except ProfilePicture.DoesNotExist:
        res['profilePicture'] = {}

    try:
        cover_picture = CoverPicture.objects.get(model=model.id, inUse=True)
        cover_picture_serializer = CoverPictureSerializer(cover_picture)
        res['coverPicture'] = cover_picture_serializer.data
    except CoverPicture.DoesNotExist:
        res['coverPicture'] = {}

    return Response(res)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_profile_picture(request, picture_id):
    model_id = request.user.model.id

    try:
        objs = [
            ProfilePicture.objects.get(pk=picture_id, model=model_id),
            ProfilePicture.objects.get(model=model_id, inUse=True)
        ]

        if objs[0].id == objs[1].id:
            res = {
                "profilePicture": ["Picture is already marked."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        objs[0].inUse = True
        objs[1].inUse = False

        ProfilePicture.objects.bulk_update(objs, ['inUse'])

        return Response()
    except ProfilePicture.DoesNotExist:
        raise Http404


class ListPorfilePictures(generics.ListAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CreatedAtPaginator

    def get_queryset(self):
        return ProfilePicture.objects.filter(model=self.request.user.model.id)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfilePictureAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return ProfilePicture.objects.get(pk=pk, model=self.request.user.model.id)
        except ProfilePicture.DoesNotExist:
            raise Http404

    def delete(self, request, picture_id):
        picture = self.get_object(picture_id)

        if picture.inUse:
            res = {
                "profilePicture": ["Can not delete current used profile picture."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        picture.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_cover_picture(request, picture_id):
    model_id = request.user.model.id

    try:
        objs = [
            CoverPicture.objects.get(pk=picture_id, model=model_id),
            CoverPicture.objects.get(model=model_id, inUse=True)
        ]

        if objs[0].id == objs[1].id:
            res = {
                "coverPicture": ["Picture is already marked."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        objs[0].inUse = True
        objs[1].inUse = False

        CoverPicture.objects.bulk_update(objs, ['inUse'])

        return Response()
    except CoverPicture.DoesNotExist:
        raise Http404


class ListCoverPictures(generics.ListAPIView):
    serializer_class = CoverPictureSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CreatedAtPaginator

    def get_queryset(self):
        return CoverPicture.objects.filter(model=self.request.user.model.id)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CoverPictureAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CoverPicture.objects.get(pk=pk, model=self.request.user.model.id)
        except CoverPicture.DoesNotExist:
            raise Http404

    def delete(self, request, picture_id):
        picture = self.get_object(picture_id)

        if picture.inUse:
            res = {
                "coverPicture": ["Can not delete current used cover picture."]
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        picture.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
