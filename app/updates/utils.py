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
