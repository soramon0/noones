from django.db import models

from models.models import (
    Model,
    AbstractMensuration,
    Mensuration,
    Photo,
)


class MeasuresUpdate(AbstractMensuration):
    # This database table is going to hold the measures update data
    # temporarily until the admin deleltes it
    measure = models.OneToOneField(
        Mensuration,
        on_delete=models.CASCADE,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    def __str__(self):
        return str(self.id)


class PhotosUpdate(models.Model):
    image = models.ImageField(upload_to='photos/updates')
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.image)
