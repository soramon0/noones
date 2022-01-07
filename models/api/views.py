from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.http import Http404
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from models.api.pagination import CreatedAtPaginator
from models.api.serializers import (
    ProfileSerializer,
    ModelContactSerializer,
    ProfilePictureWithModelSerializer,
    UserSerializer,
    MeasuresSerializer,
    ProfilePictureSerializer,
    CoverPictureSerializer,
    PhotoSerializer,
    SearchSerilaizer,
)
from models.models import (
    Profile,
    Mensuration,
    Gallery,
    ProfilePicture,
    CoverPicture,
    Contact,
)


User = get_user_model()


@api_view(("GET",))
@permission_classes((IsAuthenticated,))
def me(request):
    user = request.user
    profile = user.profile
    measures = user.mensuration

    user_serializer = UserSerializer(user)
    model_serializer = ProfileSerializer(profile)
    measures_serializer = MeasuresSerializer(measures)

    # Gallery
    photos = Gallery.objects.filter(profile=profile, inUse=True)[:8]
    photo_serializer = PhotoSerializer(photos, many=True)

    context = {
        "model": model_serializer.data,
        "measures": measures_serializer.data,
        "photos": photo_serializer.data,
    }
    context["model"].update({"email": user_serializer.data["email"]})

    try:
        profile_picture = ProfilePicture.objects.get(
            profile_id=profile.id, inUse=True)
        profile_picture_serializer = ProfilePictureSerializer(profile_picture)
        context["profilePicture"] = profile_picture_serializer.data
    except ProfilePicture.DoesNotExist:
        context["profilePicture"] = {}

    try:
        cover_picture = CoverPicture.objects.get(
            profile_id=profile.id, inUse=True)
        cover_picture_serializer = CoverPictureSerializer(cover_picture)
        context["coverPicture"] = cover_picture_serializer.data
    except CoverPicture.DoesNotExist:
        context["coverPicture"] = {}

    return Response(context)


@api_view(["POST"])
def contact_model(request):
    serializer = ModelContactSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    model_id = serializer.data.get("model_id")
    model_full_name = serializer.data.get("model_full_name")
    full_name = serializer.data.get("full_name")
    email = serializer.data.get("email")
    phone = serializer.data.get("phone")

    try:
        user = User.objects.get(profile=model_id)
        user_email = user.email
    except User.DoesNotExist:
        error = {"errors": {"model_full_name": ["model do not exist"]}}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)

    Contact.objects.create(
        user=user,
        model_full_name=model_full_name,
        full_name=full_name,
        model_email=user_email,
        email=email,
        phone=phone,
    )

    send_mail(
        f"Contact Request for {user_email}",
        f"Client {full_name} at {email} - {phone} wants to contact {user_email}",
        email,
        (settings.EMAIL_HOST_USER,),
        fail_silently=False,
    )

    return Response({"message": "Thanks! We'll get back to you soon."})


class ListModels(generics.ListAPIView):
    serializer_class = ProfilePictureWithModelSerializer

    def get_queryset(self):
        fields = (
            "image",
            "profile__first_name",
            "profile__last_name",
            "profile__country",
            "profile__city",
        )
        return (
            ProfilePicture.objects.filter(inUse=True)
            .select_related("profile")
            .only(*fields)
            .order_by("-user__created_at")
        )

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UpdateModel(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, pk=None):
        profile = self.get_object()

        data = request.data

        data.pop("bio", None)

        serializer = self.get_serializer(profile, data=data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response(serializer.data)


class SearchModels(generics.ListAPIView):
    serializer_class = ProfilePictureWithModelSerializer
    data = {}

    def get_queryset(self):
        country = self.data.get("country")
        city = self.data.get("city")
        gender = self.data.get("gender")
        hair = self.data.get("hair")
        eyes = self.data.get("eyes")
        height = self.data.get("height")

        # data is 1.40-1.60
        # split to get each one
        height = height.split("-")

        fields = (
            "image",
            "profile__first_name",
            "profile__last_name",
            "profile__country",
            "profile__city",
        )

        return ProfilePicture.objects.filter(
            inUse=True,
            profile__country__iexact=country,
            profile__city__iexact=city,
            profile__gender__iexact=gender,
            user__mensuration__hair__iexact=hair,
            user__mensuration__eyes__iexact=eyes,
            user__mensuration__height__gte=height[0],
            user__mensuration__height__lte=height[1],
        ).select_related("profile").only(*fields).order_by("-user__created_at")

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


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def mark_as_profile_picture(request, picture_id):
    user_id = request.user.id

    try:
        objs = [
            ProfilePicture.objects.get(pk=picture_id, user_id=user_id),
            ProfilePicture.objects.get(user_id=user_id, inUse=True),
        ]

        if objs[0].id == objs[1].id:
            res = {"profilePicture": ["Picture is already marked."]}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        objs[0].inUse = True
        objs[1].inUse = False

        ProfilePicture.objects.bulk_update(objs, ["inUse"])

        return Response()
    except ProfilePicture.DoesNotExist:
        raise Http404


class ListPorfilePictures(generics.ListAPIView):
    serializer_class = ProfilePictureSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CreatedAtPaginator

    def get_queryset(self):
        return ProfilePicture.objects.filter(user_id=self.request.user.id)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfilePictureAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return ProfilePicture.objects.get(pk=pk, user_id=self.request.user.id)
        except ProfilePicture.DoesNotExist:
            raise Http404

    def delete(self, request, picture_id):
        picture = self.get_object(picture_id)

        if picture.inUse:
            context = {
                "profilePicture": ["Can not delete current used profile picture."]
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        picture.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(("PUT",))
@permission_classes((IsAuthenticated,))
def mark_as_cover_picture(request, picture_id):
    user_id = request.user.id

    try:
        objs = [
            CoverPicture.objects.get(pk=picture_id, user_id=user_id),
            CoverPicture.objects.get(user_id=user_id, inUse=True),
        ]

        if objs[0].id == objs[1].id:
            res = {"coverPicture": ["Picture is already marked."]}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

        objs[0].inUse = True
        objs[1].inUse = False

        CoverPicture.objects.bulk_update(objs, ["inUse"])

        return Response()
    except CoverPicture.DoesNotExist:
        raise Http404


class ListCoverPictures(generics.ListAPIView):
    serializer_class = CoverPictureSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CreatedAtPaginator

    def get_queryset(self):
        return CoverPicture.objects.filter(user_id=self.request.user.id)

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CoverPictureAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, pk):
        try:
            return CoverPicture.objects.get(pk=pk, user_id=self.request.user.id)
        except CoverPicture.DoesNotExist:
            raise Http404

    def delete(self, request, picture_id):
        picture = self.get_object(picture_id)

        if picture.inUse:
            context = {"coverPicture": [
                "Can not delete current used cover picture."]}
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        picture.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
