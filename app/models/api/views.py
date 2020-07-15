import os

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404
from django.conf import settings
from django.core.mail import send_mail


from core.models import User
from models.models import (
    Model,
    Mensuration,
    Photo,
    ProfilePicture,
    CoverPicture,
    Contact
)
from models.api.serializers import (
    ModelSerializer,
    ModelContactSerializer,
    ProfilePictureWithModelSerializer,
    UserSerializer,
    MeasuresSerializer,
    ProfilePictureSerializer,
    CoverPictureSerializer,
    PhotoSerializer,
    SearchSerilaizer
)
from models.api.pagination import CreatedAtPaginator


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


@api_view(['POST'])
def model_contact(request):
    serializer = ModelContactSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    model_id = serializer.data.get('model_id')
    model_full_name = serializer.data.get('model_full_name')
    full_name = serializer.data.get('full_name')
    email = serializer.data.get('email')
    phone = serializer.data.get('phone')

    try:
        model = Model.objects.only('user').get(pk=model_id)
        model_email = model.user.email
    except Model.DoesNotExist:
        error = {'errors': {'model_full_name': ['model do not exist']}}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    Contact.objects.create(model=model, model_full_name=model_full_name, full_name=full_name,
                           model_email=model_email, email=email, phone=phone)

    send_mail(
        f'Contact Request for {model_email}',
        f'Client {full_name} at {email} - {phone} wants to contact {model_email}',
        email,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )

    return Response({'message': "Thanks! We'll get back to you soon."})


class ListModels(generics.ListAPIView):
    serializer_class = ProfilePictureWithModelSerializer

    def get_queryset(self):
        fields = ['image', 'model__first_name',
                  'model__last_name', 'model__country', 'model__city']
        return ProfilePicture.objects.filter(inUse=True).select_related('model').only(*fields).order_by('-model__created_at')

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SearchModels(generics.ListAPIView):
    serializer_class = ProfilePictureWithModelSerializer
    data = {}

    def get_queryset(self):
        pays = self.data.get('pays')
        ville = self.data.get('ville')
        sexe = self.data.get('sexe')
        cheveux = self.data.get('cheveux')
        yeux = self.data.get('yeux')
        taille = self.data.get('taille')

        # data is 1.40-1.60
        # split to get each one
        taille = taille.split('-')

        fields = ['image', 'model__first_name',
                  'model__last_name', 'model__country', 'model__city']
        return ProfilePicture.objects.filter(
            inUse=True, model__country__iexact=pays, model__city__iexact=ville,
            model__sexe__iexact=sexe, model__measures__cheveux__iexact=cheveux,
            model__measures__yeux__iexact=yeux, model__measures__taille__gte=taille[0],
            model__measures__taille__lte=taille[1]
        ).select_related('model').only(*fields).order_by('-model__created_at')

    def set_data(self, data):
        self.data = data

    def list(self, request):
        serializer = SearchSerilaizer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.set_data(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@ api_view(['PUT'])
@ permission_classes([IsAuthenticated])
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
