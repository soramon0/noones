from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from models.api.serializers import PhotoSerializer
from models.models import (
    Mensuration,
    Photo,
    ProfilePicture,
    CoverPicture,
)
from updates.models import (
    MeasuresUpdate,
    PhotosUpdate,
    ProfilePictureUpdate,
    CoverPictureUpdate,
)


@receiver(post_save, sender=MeasuresUpdate)
def apply_measures_update(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        # if the admin sets the accept field to true
        # then we apply the update to the original table
        if instance.accept and not instance.decline:
            Mensuration.objects.filter(
                pk=instance.measure_id).update(taille=instance.taille, taillenombrill=instance.taillenombrill, buste=instance.buste, epaules=instance.epaules,
                                               hanches=instance.hanches, poids=instance.poids, pointure=instance.pointure, cheveux=instance.cheveux, yeux=instance.yeux,)


@receiver(post_save, sender=PhotosUpdate)
def apply_gallery_update(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        if instance.accept and not instance.decline:
            if not instance.related_photo:
                photo = Photo.objects.create(image=instance.image, inUse=True,
                                             model=instance.model)
                instance.related_photo = photo
                instance.save()
            else:
                photo = instance.related_photo
                photo.image = instance.image
                photo.save()


@receiver(post_delete, sender=PhotosUpdate)
def delete_old_gallery_photo_update(sender, instance, using, **kwargs):
    photo = instance.related_photo
    if not photo:
        # if no related_photo then just delete the photo
        PhotoSerializer.delete_old_image(instance.image)

    elif instance.image.path != photo.image.path:
        # if we have a related photo and the photo_update
        # does not point to the same image as the original
        PhotoSerializer.delete_old_image(instance.image)


@receiver(post_save, sender=ProfilePictureUpdate)
def apply_profile_picture_update(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        if instance.accept and not instance.decline:
            model = instance.model
            try:
                ProfilePicture.objects.filter(
                    model=model.id, inUse=True).update(inUse=False)
            except ProfilePicture.DoesNotExit:
                pass

            ProfilePicture.objects.create(
                model=model, inUse=True, image=instance.image)


@receiver(post_delete, sender=ProfilePictureUpdate)
def delete_old_profile_picture_update(sender, instance, using, **kwargs):
    query = ProfilePicture.objects.filter(
        model=instance.model, image=instance.image)
    if not query.exists():
        PhotoSerializer.delete_old_image(instance.image)


@receiver(post_save, sender=CoverPictureUpdate)
def apply_cover_picture_update(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        if instance.accept and not instance.decline:
            model = instance.model
            try:
                CoverPicture.objects.filter(
                    model=model.id, inUse=True).update(inUse=False)
            except ProfilePicture.DoesNotExit:
                pass

            CoverPicture.objects.create(
                model=model, inUse=True, image=instance.image)


@receiver(post_delete, sender=CoverPictureUpdate)
def delete_old_cover_picture_update(sender, instance, using, **kwargs):
    query = CoverPicture.objects.filter(
        model=instance.model, image=instance.image)
    if not query.exists():
        PhotoSerializer.delete_old_image(instance.image)
