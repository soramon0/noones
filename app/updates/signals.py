from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

from models.api.serializers import PhotoSerializer
from core.utils import delete_file
from models.models import (
    Profile,
    Mensuration,
    Gallery,
    ProfilePicture,
    CoverPicture,
)
from updates.models import (
    ProfileUpdate,
    MeasuresUpdate,
    GalleryUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)
from updates.tasks import image_resize_task


@receiver(post_save, sender=ProfileUpdate)
def apply_model_update(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        # Send Email to admin
        # TODO(karim): Update this email
        send_mail(
            f"Update Request from {instance.user.email}",
            "New Update request for model",
            instance.user.email,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
    else:
        if instance.accept and not instance.decline:
            Profile.objects.filter(
                pk=instance.profile.id).update(bio=instance.bio)


@receiver(post_save, sender=MeasuresUpdate)
def apply_measures_update(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if not created:
        # if the admin sets the accept field to true
        # then we apply the update to the original table
        if instance.accept and not instance.decline:
            m = instance.measures
            print(instance.measures_id)
            Mensuration.objects.filter(pk=instance.measures.id).update(
                height=instance.height,
                waist=instance.waist,
                bust=instance.bust,
                shoulders=instance.shoulders,
                hips=instance.hips,
                weight=instance.weight,
                shoe_size=instance.shoe_size,
                hair=instance.hair,
                eyes=instance.eyes,
            )


@receiver(post_save, sender=GalleryUpdate)
def apply_gallery_update(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if created:
        image_resize_task.delay(instance.image.path, 1280, 720)
    else:
        if instance.accept and not instance.decline:
            if not instance.related_photo:
                photo = Gallery.objects.create(
                    image=instance.image,
                    inUse=True,
                    user=instance.user,
                    profile=instance.user.profile,
                )

                # save the realted photo on this instance using a update query
                # so that we do not trigger this signal again
                GalleryUpdate.objects.filter(
                    id=instance.id).update(related_photo=photo)
            else:
                # update the one we have by deleting the old picture
                # and pointing the one we have to the new picture
                photo = instance.related_photo
                old_image = photo.image
                if old_image.path != instance.image.path:
                    delete_file(old_image)
                photo.image = instance.image
                photo.save()


@receiver(post_delete, sender=GalleryUpdate)
def delete_old_gallery_photo_update(sender, instance, using, **kwargs):
    try:
        photo = instance.related_photo
        if not photo:
            # if no related_photo then just delete the photo
            delete_file(instance.image)

        elif instance.image.path != photo.image.path:
            # if we have a related photo and the photo_update
            # does not point to the same image as the original
            delete_file(instance.image)
    except Gallery.DoesNotExist:
        delete_file(instance.image)


@receiver(post_save, sender=ProfilePictureUpdate)
def apply_profile_picture_update(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if created:
        image_resize_task.delay(instance.image.path, 720, 900, by_wdith=True)
    else:
        if instance.accept and not instance.decline:
            user = instance.user
            try:
                # if user already has a profile picture
                # set it's inUse value to false
                ProfilePicture.objects.filter(
                    user=user, inUse=True).update(inUse=False)
            except ProfilePicture.DoesNotExit:
                pass

            ProfilePicture.objects.create(
                user=user, profile=user.profile, image=instance.image, inUse=True
            )


@receiver(post_delete, sender=ProfilePictureUpdate)
def delete_old_profile_picture_update(sender, instance, using, **kwargs):
    query = ProfilePicture.objects.filter(
        user=instance.user, image=instance.image)
    if not query.exists():
        delete_file(instance.image)


@receiver(post_save, sender=CoverPictureUpdate)
def apply_cover_picture_update(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if created:
        image_resize_task.delay(instance.image.path, 1280, 720)
    else:
        if instance.accept and not instance.decline:
            user = instance.user
            try:
                CoverPicture.objects.filter(
                    user=user, inUse=True).update(inUse=False)
            except ProfilePicture.DoesNotExit:
                pass

            CoverPicture.objects.create(
                user=user, profile=user.profile, inUse=True, image=instance.image
            )


@receiver(post_delete, sender=CoverPictureUpdate)
def delete_old_cover_picture_update(sender, instance, using, **kwargs):
    query = CoverPicture.objects.filter(
        user=instance.user, image=instance.image)
    if not query.exists():
        delete_file(instance.image)
