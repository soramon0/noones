from django.db.models.signals import post_save
from django.dispatch import receiver
from updates.models import MeasuresUpdate
from models.models import Mensuration


@receiver(post_save, sender=MeasuresUpdate)
def handle_admin_action(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        # if the admin sets the accept field to true
        # then we apply the update to the original table
        if instance.accept and not instance.decline:
            Mensuration.objects.filter(
                pk=instance.measure_id).update(taille=instance.taille, taillenombrill=instance.taillenombrill, buste=instance.buste, epaules=instance.epaules,
                                               hanches=instance.hanches, poids=instance.poids, pointure=instance.pointure, cheveux=instance.cheveux, yeux=instance.yeux,)
