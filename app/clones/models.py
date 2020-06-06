from django.db import models

from models.models import (
    Model,
    AbstractMensuration,
    Mensuration,
    Photo,
)

# This database table is going to hold the measures update data
# temporarily until the admin deleltes it
class MeasuresClone(AbstractMensuration):
    measure = models.OneToOneField(
        Mensuration,
        on_delete=models.DO_NOTHING,
    )

    def __str__(self):
        return str(self.id)

class PhotoClone(models.Model):
    image = models.ImageField(upload_to='photos/updates')
    original = models.OneToOneField(Photo, on_delete=models.DO_NOTHING)
