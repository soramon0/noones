from django.db import models

from models.models import (
    Model,
    AbstractMensuration,
    Mensuration,
    Photo,
)


class ModelUpdate(models.Model):
    # This database table is going to hold the model update data
    # temporarily until the admin deletes it
    model = models.OneToOneField(
        Model,
        on_delete=models.CASCADE,
    )
    bio = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Model Updates"

    def __str__(self):
        return str(self.id)


class MeasuresUpdate(AbstractMensuration):
    # This database table is going to hold the measures update data
    # temporarily until the admin deletes it
    measure = models.OneToOneField(
        Mensuration,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Measure Updates"

    def __str__(self):
        return str(self.id)


class PhotosUpdate(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    related_photo = models.ForeignKey(
        Photo, null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Gallery Updates"

    def __str__(self):
        return self.image.url


class ProfilePictureUpdate(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Profile Picture Updates"

    def __str__(self):
        return self.image.url


class CoverPictureUpdate(models.Model):
    image = models.ImageField(upload_to='photos/%Y/%m/%d')
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Cover Picture Updates"

    def __str__(self):
        return self.image.url
