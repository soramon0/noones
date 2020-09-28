from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from models.models import Gallery, ProfilePicture, CoverPicture
from updates.models import GalleryUpdate
from updates.tasks import image_resize_task
from core.utils import delete_file


@receiver(post_delete, sender=Gallery)
def delete_old_gallery_photo(sender, instance, using, **kwargs):
    # TODO(karim): check if any updates uses this image
    delete_file(instance.image)


@receiver(post_save, sender=ProfilePicture)
def handle_pp_post_save(
    sender, instance, created, raw, using, update_fields, **kwargs
):
    if created:
        image_resize_task.delay(instance.image.path, 720, 900, by_wdith=True)


@receiver(post_delete, sender=ProfilePicture)
def delete_old_profile_picture(sender, instance, using, **kwargs):
    # TODO(karim): check if any updates uses this image
    delete_file(instance.image)


@receiver(post_delete, sender=CoverPicture)
def delete_old_cover_picture(sender, instance, using, **kwargs):
    # TODO(karim): check if any updates uses this image
    delete_file(instance.image)
