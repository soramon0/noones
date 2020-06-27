from django.db.models.signals import post_delete
from django.dispatch import receiver
from models.models import Photo, ProfilePicture, CoverPicture
from models.api.serializers import PhotoSerializer
from updates.models import PhotosUpdate, Model


@receiver(post_delete, sender=Photo)
def delete_old_gallery_photo(sender, instance, using, **kwargs):
    try:
        photo_update = PhotosUpdate.objects.filter(
            related_photo=instance.id).get()

        # if no update is using the photo then we delete it
        if photo_update.image.path != instance.image.path:
            PhotoSerializer.delete_old_image(instance.image)

        # Doing an update instead of a save so that
        # we don't trigger the post_save signal on PhotosUpdate
        PhotosUpdate.objects.filter(
            id=photo_update.id).update(related_photo=None)
    except PhotosUpdate.DoesNotExist:
        PhotoSerializer.delete_old_image(instance.image)


@receiver(post_delete, sender=ProfilePicture)
def delete_old_profile_picture(sender, instance, using, **kwargs):
    PhotoSerializer.delete_old_image(instance.image)


@receiver(post_delete, sender=CoverPicture)
def delete_old_cover_picture(sender, instance, using, **kwargs):
    PhotoSerializer.delete_old_image(instance.image)
