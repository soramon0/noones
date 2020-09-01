from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from django.conf import settings

from core.utils import image_resize

logger = get_task_logger(__name__)


@shared_task()
def email_send(email):
    logger.info('sending email')
    send_mail(
        f"User {email} deleted his update",
        "Delete request for measures update",
        email,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )


@shared_task()
def image_resize_task(path, width, height, by_wdith=False):
    return image_resize(path=path, width=width, height=height, by_wdith=by_wdith)
