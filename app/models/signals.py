from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Model

# TODO(karim): add a post_delete to Model to clean it's images after deletion
# TODO(karim): add a post_delete to Photo to clean it's images after deletion
@receiver(post_save, sender=Model)
def delete_old_photo(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created and instance.profilePicture:
        print(instance.profilePicture.path)
