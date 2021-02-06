from django.utils import timezone

from core.models import User
from models.models import Gallery
from rest_framework.exceptions import ValidationError


def check_upload_count(*, owner: User, images: list):
    """
    check and make sure that the user can not upload more than 8 images.
    """
    MAX_GALLERY_UPLOAD_COUNT = 8
    images_to_upload = len(images)
    gallery_count = Gallery.objects.filter(user=owner).count()

    if (gallery_count + images_to_upload) > MAX_GALLERY_UPLOAD_COUNT:
        msg = f"You can only upload {MAX_GALLERY_UPLOAD_COUNT} photos; you've uploaded {gallery_count} so far."
        context = {"gallery": [msg]}
        raise ValidationError(context)


def updates_task_format_log(*, name: str, count: int, obj: dict):
    context = {}

    if count != 0:
        for key, value in obj.items():
            context['type'] = name
            context['delete_count'] = value
    else:
        context = {'type': name,  'delete_count': count}

    return context


class UpdateChecks:
    def is_update_accepted(self, field: str):
        """
        if the update has been accepted, the user should not be able to change it.
        """
        if self.accept:
            msg = "this update has already been accepted and will be deleted in the next 24h."
            context = {field: [msg]}
            raise ValidationError(context)

    def is_update_within_a_day(self, field: str):
        """
        Update permission is only allowed if it hasn't been 24 hours.
        But if the request was delined the user can update the request again for the next 24 hours
        """
        if not self.decline:
            now = timezone.now()
            days = (now - self.created_at).days

            if days != 0:
                msg = "You can only update within the first 24 hours."
                context = {field: [msg]}
                raise ValidationError(context)
