import uuid
from typing import Iterator

from django.http import Http404

from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)
from core.models import User


def get_profile_update(*, fetched_by: User, pk: uuid.UUID = None) -> ProfileUpdate:
    try:
        if pk is None:
            return ProfileUpdate.objects.filter(user=fetched_by).get()
        return ProfileUpdate.objects.filter(user=fetched_by, pk=pk).get()
    except ProfileUpdate.DoesNotExist:
        raise Http404


def get_measures_update(*, fetched_by: User, pk: uuid.UUID = None) -> MeasuresUpdate:
    try:
        if pk is None:
            return MeasuresUpdate.objects.filter(user=fetched_by).get()
        return MeasuresUpdate.objects.filter(user=fetched_by, pk=pk).get()
    except MeasuresUpdate.DoesNotExist:
        raise Http404


def get_gallery_update(
    *, fetched_by: User, pk: uuid.UUID = None, related_photo=None
) -> GalleryUpdate:
    if related_photo is not None:
        return GalleryUpdate.objects.filter(
            user=fetched_by, related_photo=related_photo
        ).get()
    try:
        if pk is None:
            return GalleryUpdate.objects.filter(user=fetched_by).get()
        return GalleryUpdate.objects.filter(user=fetched_by, pk=pk).get()
    except GalleryUpdate.DoesNotExist:
        raise Http404


def get_gallery_updates(*, fetched_by: User) -> Iterator[GalleryUpdate]:
    return GalleryUpdate.objects.filter(user=fetched_by)


def get_profile_picture_update(
    *, fetched_by: User, pk: uuid.UUID = None
) -> ProfilePictureUpdate:
    try:
        if pk is None:
            return ProfilePictureUpdate.objects.filter(user=fetched_by).get()
        return ProfilePictureUpdate.objects.filter(user=fetched_by, pk=pk).get()
    except ProfilePictureUpdate.DoesNotExist:
        raise Http404


def get_profile_picture_updates(*, fetched_by: User) -> Iterator[ProfilePictureUpdate]:
    return ProfilePictureUpdate.objects.filter(user=fetched_by)


def get_cover_picture_update(
    *, fetched_by: User, pk: uuid.UUID = None
) -> CoverPictureUpdate:
    try:
        if pk is None:
            return CoverPictureUpdate.objects.filter(user=fetched_by).get()
        return CoverPictureUpdate.objects.filter(user=fetched_by, pk=pk).get()
    except CoverPictureUpdate.DoesNotExist:
        raise Http404


def get_cover_picture_updates(*, fetched_by: User) -> Iterator[CoverPictureUpdate]:
    return CoverPictureUpdate.objects.filter(user=fetched_by)


def get_cover_picture_updates(*, fetched_by: User) -> Iterator[CoverPictureUpdate]:
    return CoverPictureUpdate.objects.filter(user=fetched_by)