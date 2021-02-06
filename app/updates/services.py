import uuid
from datetime import timedelta

from django.utils import timezone
from rest_framework.exceptions import NotFound

from core.models import User
from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)
from updates.utils import check_upload_count
from core.utils import delete_file


def create_profile_update(
    *,
    user: uuid.UUID,
    profile: uuid.UUID,
    bio: str,
) -> ProfileUpdate:
    return ProfileUpdate.objects.create(bio=bio, user_id=user, profile_id=profile)


def delete_profile_update(*, fetched_by: User, pk: uuid.UUID):
    count, _ = ProfileUpdate.objects.filter(user=fetched_by, pk=pk).delete()
    if count == 0:
        raise NotFound()


def delete_all_profile_updates() -> tuple:
    '''
        delete all profile updates that are one day old or more
    '''
    yesterday = timezone.now() - timedelta(days=1)

    return ProfileUpdate.objects.filter(
        accept=True, created_at__date__lte=yesterday).delete()


def modify_profile_update(*, update: ProfileUpdate, bio: str) -> ProfileUpdate:
    update.bio = bio
    update.message = ""
    update.dirty = True
    update.decline = None
    update.save()
    return update


def create_measures_update(
    *,
    user: uuid.UUID,
    measures: uuid.UUID,
    height: int,
    waist: int,
    bust: int,
    shoulders: int,
    hips: int,
    weight: int,
    shoe_size: int,
    hair: str,
    eyes: str,
) -> MeasuresUpdate:
    return MeasuresUpdate.objects.create(
        height=height,
        waist=waist,
        bust=bust,
        shoulders=shoulders,
        hips=hips,
        weight=weight,
        shoe_size=shoe_size,
        hair=hair,
        eyes=eyes,
        user_id=user,
        measures_id=measures,
    )


def delete_measures_update(*, fetched_by: User, pk: uuid.UUID):
    count, _ = MeasuresUpdate.objects.filter(user=fetched_by, pk=pk).delete()
    if count == 0:
        raise NotFound()


def delete_all_measures_updates() -> tuple:
    '''
        delete all measures updates that are one day old or more
    '''
    yesterday = timezone.now() - timedelta(days=1)

    return MeasuresUpdate.objects.filter(
        accept=True, created_at__date__lte=yesterday).delete()


def modify_measures_update(
    *,
    update: ProfileUpdate,
    height: int,
    waist: int,
    bust: int,
    shoulders: int,
    hips: int,
    weight: int,
    shoe_size: int,
    hair: str,
    eyes: str,
) -> MeasuresUpdate:
    update.message = ""
    update.decline = None
    update.created_at = timezone.now()
    update.height = height
    update.waist = waist
    update.bust = bust
    update.shoulders = shoulders
    update.hips = hips
    update.weight = weight
    update.shoe_size = shoe_size
    update.hair = hair
    update.eyes = eyes
    update.save()
    return update


def create_gallery_update(*, owner: User, image, related_photo=None) -> GalleryUpdate:
    if related_photo is not None:
        return GalleryUpdate.objects.create(
            user=owner, image=image, related_photo_id=related_photo
        )
    return GalleryUpdate.objects.create(user=owner, image=image)


def delete_gallery_update(*, fetched_by: User, pk: uuid.UUID):
    count, _ = GalleryUpdate.objects.filter(user=fetched_by, pk=pk).delete()
    if count == 0:
        raise NotFound()


def delete_all_gallery_updates() -> tuple:
    '''
        delete all gallery updates that are one day old or more
    '''
    yesterday = timezone.now() - timedelta(days=1)

    return GalleryUpdate.objects.filter(
        accept=True, created_at__date__lte=yesterday).delete()


def modify_gallery_update(*, update: GalleryUpdate, image) -> GalleryUpdate:
    old_image = update.image
    update.message = ""
    update.decline = None
    update.created_at = timezone.now()
    update.image = image
    update.save()
    delete_file(old_image)
    return update


def reset_gallery_update(*, update: GalleryUpdate, image) -> GalleryUpdate:
    # get a refrence to the old image to compare against later
    old_image = update.image

    update.created_at = timezone.now()
    update.accept = None
    update.decline = None
    update.message = ""
    update.image = image
    update.save()

    # check that the old image is not refrenced anymore
    # by the update or the gallery
    currently_used_image = update.related_photo.image.path
    if old_image.path != currently_used_image and old_image.path != update.image.path:
        delete_file(old_image)

    return update


def create_profile_picture_update(*, owner: User, image) -> ProfilePictureUpdate:
    return ProfilePictureUpdate.objects.create(user=owner, image=image)


def delete_profile_picture_update(*, fetched_by: User, pk: uuid.UUID):
    count, _ = ProfilePictureUpdate.objects.filter(
        user=fetched_by, pk=pk).delete()
    if count == 0:
        raise NotFound()


def modify_profile_picturey_update(
    *, update: ProfilePictureUpdate, image
) -> ProfilePictureUpdate:
    old_image = update.image
    update.message = ""
    update.decline = None
    update.created_at = timezone.now()
    update.image = image
    update.save()
    delete_file(old_image)
    return update


def delete_all_profile_picture_updates() -> tuple:
    '''
        delete all profile pictures updates that are one day old or more
    '''
    yesterday = timezone.now() - timedelta(days=1)

    return ProfilePictureUpdate.objects.filter(
        accept=True, created_at__date__lte=yesterday).delete()


def create_cover_picture_update(*, owner: User, image) -> CoverPictureUpdate:
    return CoverPictureUpdate.objects.create(user=owner, image=image)


def delete_cover_picture_update(*, fetched_by: User, pk: uuid.UUID):
    count, _ = CoverPictureUpdate.objects.filter(
        user=fetched_by, pk=pk).delete()
    if count == 0:
        raise NotFound()


def delete_all_cover_picture_updates() -> tuple:
    '''
        delete all cover pictures updates that are one day old or more
    '''
    yesterday = timezone.now() - timedelta(days=1)

    return CoverPictureUpdate.objects.filter(
        accept=True, created_at__date__lte=yesterday).delete()


def modify_cover_picturey_update(
    *, update: CoverPictureUpdate, image
) -> CoverPictureUpdate:
    old_image = update.image
    update.message = ""
    update.decline = None
    update.created_at = timezone.now()
    update.image = image
    update.save()
    delete_file(old_image)
    return update
