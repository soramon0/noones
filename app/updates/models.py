import uuid

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from models.models import (
    Profile,
    AbstractMensuration,
    Mensuration,
    Gallery,
)


class BaseUpdates(models.Model):
    class Meta:
        abstract = True

    def is_update_accepted(self, field: str):
        """
        if the update has been accepted, the user should not be able to change it.
        """
        # pylint: disable=no-member
        if self.accept:
            msg = "this update has already been accepted and will be deleted in the next 24h."
            context = {field: [msg]}
            raise ValidationError(context)

    def purify(self):
        self.dirty = False
        self.save()


class ProfileUpdate(BaseUpdates):
    # This database table is going to hold the model update data
    # temporarily until the admin deletes it
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    # keeps track of whether an update has been changed or not
    dirty = models.BooleanField(default=False)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    @staticmethod
    def update_exists(self, id: uuid.UUID):
        if self.objects.filter(user_id=id).exists():
            msg = "do not create a new upadte request! Update the one you have."
            context = {"model": [msg]}
            raise ValidationError(context)

    class Meta:
        verbose_name_plural = "Model Updates"

    def __str__(self):
        return str(self.id)


class MeasuresUpdate(AbstractMensuration, BaseUpdates):
    # This database table is going to hold the measures update data
    # temporarily until the admin deletes it
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    measures = models.OneToOneField(Mensuration, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    # keeps track of whether an update has been changed or not
    dirty = models.BooleanField(default=False)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    @staticmethod
    def update_exists(self, id: uuid.UUID):
        if self.objects.filter(user_id=id).exists():
            msg = "do not create a new upadte request! Update the one you have."
            context = {"measures": [msg]}
            raise ValidationError(context)

    class Meta:
        verbose_name_plural = "Measure Updates"

    def __str__(self):
        return str(self.id)


class GalleryUpdate(BaseUpdates):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    related_photo = models.OneToOneField(
        Gallery, null=True, blank=True, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    changed_at = models.DateTimeField(auto_now=True)
    # keeps track of whether an update has been changed or not
    dirty = models.BooleanField(default=False)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    @staticmethod
    def get_images(data) -> list:
        try:
            images = data.getlist("image")
            return images
        except AttributeError:
            msg = "No file was submitted."
            context = {"model": [msg]}
            raise ValidationError(context)

    class Meta:
        verbose_name_plural = "Gallery Updates"

    def __str__(self):
        return self.image.url


class ProfilePictureUpdate(BaseUpdates):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(auto_now=True)
    # keeps track of whether an update has been changed or not
    dirty = models.BooleanField(default=False)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Profile Picture Updates"

    def __str__(self):
        return self.image.url


class CoverPictureUpdate(BaseUpdates):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="photos/%Y/%m/%d")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    changed_at = models.DateTimeField(auto_now=True)
    # keeps track of whether an update has been changed or not
    dirty = models.BooleanField(default=False)
    accept = models.BooleanField(null=True, blank=True)
    decline = models.BooleanField(null=True, blank=True)
    message = models.TextField(max_length=500, blank=True, default="")

    class Meta:
        verbose_name_plural = "Cover Picture Updates"

    def __str__(self):
        return self.image.url
