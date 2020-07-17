from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def apply_measures_update(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        pass
