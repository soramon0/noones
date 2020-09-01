from rest_framework import status, viewsets, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings

from core.mixins import ApiErrorsMixin
from models.models import Gallery
from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
)
from updates.utils import check_upload_count
from updates.api.serializers import (
    OutputProfileUpdateSerializer,
    InputProfileUpdateSerializer,
    OutputMeasuresUpdateSerializer,
    InputMeasuresUpdateSerializer,
    OutputGalleryUpdateSerializer,
    InputGalleryUpdateSerializer,
    OutputProfilePictureUpdateSerializer,
    InputProfilePictureUpdateSerializer,
    OutputCoverPictureUpdateSerializer,
    InputCoverPictureUpdateSerializer,
)
from updates.selectos import (
    get_cover_picture_update,
    get_cover_picture_updates,
    get_gallery_update,
    get_gallery_updates,
    get_measures_update,
    get_profile_picture_update,
    get_profile_picture_updates,
    get_profile_update,
)
from updates.services import (
    create_cover_picture_update,
    create_gallery_update,
    create_measures_update,
    create_profile_picture_update,
    create_profile_update,
    delete_cover_picture_update,
    delete_gallery_update,
    delete_measures_update,
    delete_profile_picture_update,
    delete_profile_update,
    modify_cover_picturey_update,
    modify_gallery_update,
    modify_measures_update,
    modify_profile_picturey_update,
    modify_profile_update,
    reset_gallery_update,
)

from updates.tasks import email_send


class ProfileUpdateViewSet(ApiErrorsMixin, viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        profile_update = get_profile_update(fetched_by=request.user)
        serializer = OutputProfileUpdateSerializer(profile_update)
        return Response(serializer.data)

    def create(self, request):
        user = request.user

        ProfileUpdate.update_exists(ProfileUpdate, user.id)

        serializer = InputProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile_update = create_profile_update(
            user=user.id, profile=user.profile.id, **serializer.data
        )

        serializer = OutputProfileUpdateSerializer(profile_update)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = get_profile_update(fetched_by=request.user, pk=pk)

        instance.check_update_accepted(field="model")
        instance.check_update_within_a_day(field="model")

        serializer = InputProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        profile_update = modify_profile_update(
            update=instance, **serializer.data)
        serializer = OutputProfileUpdateSerializer(profile_update)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        delete_profile_update(fetched_by=request.user, pk=pk)

        # Send Email to admin
        # TODO(karim): Update this email
        email_send.delay(request.user.email)
        # send_mail(
        #     f"User {request.user.email} deleted his update",
        #     "Delete request for measures update",
        #     request.user.email,
        #     [settings.EMAIL_HOST_USER],
        #     fail_silently=False,
        # )

        return Response(status=status.HTTP_204_NO_CONTENT)


class MeasuresUpdateViewSet(ApiErrorsMixin, viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        instance = get_measures_update(fetched_by=request.user)
        serializer = OutputMeasuresUpdateSerializer(instance)
        return Response(serializer.data)

    def create(self, request):
        user = request.user

        MeasuresUpdate.update_exists(MeasuresUpdate, user.id)

        serializer = InputMeasuresUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        measures_update = create_measures_update(
            user=user.id, measures=user.mensuration.id, **serializer.data
        )
        serializer = OutputMeasuresUpdateSerializer(measures_update)

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f"Update Request from {user.email}",
            "New Update request for measures",
            user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        instance = get_measures_update(fetched_by=request.user, pk=pk)

        instance.check_update_accepted(field="measures")
        instance.check_update_within_a_day(field="measures")

        serializer = InputMeasuresUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        measures_update = modify_measures_update(
            update=instance, **serializer.data)
        serializer = OutputMeasuresUpdateSerializer(measures_update)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        delete_measures_update(fetched_by=request.user, pk=pk)

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f"User {request.user.email} deleted his update",
            "Delete request for measures update",
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class GalleryUpdateViewSet(ApiErrorsMixin, viewsets.ViewSet):
    """
    takes care of retrieving/updating/deleting one gallery update
    """

    permission_classes = (IsAuthenticated,)

    def list(self, request):
        gallery_updates = get_gallery_updates(fetched_by=request.user)
        serializer = OutputGalleryUpdateSerializer(gallery_updates, many=True)
        return Response(serializer.data)

    def create(self, request):
        images = GalleryUpdate.get_images(data=request.data)
        # A list to keep track of all uploaded images
        uploaded_images = []

        check_upload_count(owner=request.user, images=images)

        for image in images:
            data = {"image": image}
            serializer = InputGalleryUpdateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            gallery_update = create_gallery_update(owner=request.user, **data)
            serializer = OutputGalleryUpdateSerializer(gallery_update)
            uploaded_images.append(serializer.data)

        return Response(uploaded_images, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        instance = get_gallery_update(fetched_by=request.user, pk=pk)
        serializer = OutputGalleryUpdateSerializer(instance)
        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_gallery_update(fetched_by=request.user, pk=pk)

        instance.check_update_accepted(field="image")
        instance.check_update_within_a_day(field="image")

        # Only update the image field
        data = {"image": request.data.get("image", None)}

        serializer = InputGalleryUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        gallery_update = modify_gallery_update(update=instance, **data)
        serializer = OutputGalleryUpdateSerializer(gallery_update)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        delete_gallery_update(fetched_by=request.user, pk=pk)

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f"User {request.user.email} deleted his update",
            "Delete request for photo update",
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangeOrCreateGalleryUpdate(ApiErrorsMixin, APIView):
    """
    Given a gallery related photo id, find a gallery update and change it's image with the new one.
    otherwise, create a new gallery update
    """

    permission_classes = (IsAuthenticated,)

    def put(self, request, related_photo_id=None):
        user = request.user
        data = {"image": request.data.get("image", None)}

        try:
            instance = get_gallery_update(
                fetched_by=user, related_photo=related_photo_id
            )

            serializer = InputGalleryUpdateSerializer(data=data)

            serializer.is_valid(raise_exception=True)

            gallery_update = reset_gallery_update(update=instance, **data)
            serializer = OutputGalleryUpdateSerializer(gallery_update)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except GalleryUpdate.DoesNotExist:
            # check that we have a picture with the given id
            if not Gallery.objects.filter(pk=related_photo_id, user=user).exists():
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = InputGalleryUpdateSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            data["related_photo"] = related_photo_id
            gallery_update = create_gallery_update(owner=user, **data)
            serializer = OutputGalleryUpdateSerializer(gallery_update)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfilePictureUpdateViewSet(ApiErrorsMixin, viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        pp_update = get_profile_picture_updates(fetched_by=request.user)
        serializer = OutputProfilePictureUpdateSerializer(pp_update, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = {"image": request.data.get("image", None)}
        serializer = InputProfilePictureUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        pp_update = create_profile_picture_update(owner=request.user, **data)
        serializer = OutputProfilePictureUpdateSerializer(pp_update)

        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_profile_picture_update(fetched_by=request.user, pk=pk)

        instance.check_update_accepted(field="image")
        instance.check_update_within_a_day(field="image")

        # Only update the image field
        data = {"image": request.data.get("image", None)}

        serializer = InputProfilePictureUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        pp_update = modify_profile_picturey_update(update=instance, **data)
        serializer = OutputProfilePictureUpdateSerializer(pp_update)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = delete_profile_picture_update(
            fetched_by=request.user, pk=pk)

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f"User {request.user.email} deleted his update",
            "Delete request for profile photo update",
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)


class CoverPictureUpdateViewSet(ApiErrorsMixin, viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        pp_update = get_cover_picture_updates(fetched_by=request.user)
        serializer = OutputCoverPictureUpdateSerializer(pp_update, many=True)
        return Response(serializer.data)

    def create(self, request):
        data = {"image": request.data.get("image", None)}
        serializer = InputCoverPictureUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        cp_update = create_cover_picture_update(owner=request.user, **data)
        serializer = OutputCoverPictureUpdateSerializer(cp_update)

        return Response(serializer.data)

    def update(self, request, pk=None):
        instance = get_cover_picture_update(fetched_by=request.user, pk=pk)

        instance.check_update_accepted(field="image")
        instance.check_update_within_a_day(field="image")

        # Only update the image field
        data = {"image": request.data.get("image", None)}

        serializer = InputCoverPictureUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        cp_update = modify_cover_picturey_update(update=instance, **data)
        serializer = OutputProfilePictureUpdateSerializer(cp_update)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        instance = delete_cover_picture_update(fetched_by=request.user, pk=pk)

        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f"User {request.user.email} deleted his update",
            "Delete request for profile photo update",
            request.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        return Response(status=status.HTTP_204_NO_CONTENT)
