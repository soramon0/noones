from django.db.models.signals import post_delete
from django.dispatch import receiver
from models.models import Gallery, ProfilePicture, CoverPicture
from updates.models import GalleryUpdate
from core.utils import delete_file


@receiver(post_delete, sender=Gallery)
def delete_old_gallery_photo(sender, instance, using, **kwargs):
    delete_file(instance.image)


@receiver(post_delete, sender=ProfilePicture)
def delete_old_profile_picture(sender, instance, using, **kwargs):
    delete_file(instance.image)


@receiver(post_delete, sender=CoverPicture)
def delete_old_cover_picture(sender, instance, using, **kwargs):
    delete_file(instance.image)
