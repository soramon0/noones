from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task, group
from celery.utils.log import get_task_logger

from core.utils import image_resize
from updates.services import (
    delete_all_cover_picture_updates,
    delete_all_gallery_updates,
    delete_all_measures_updates,
    delete_all_profile_picture_updates,
    delete_all_profile_updates
)
from updates.utils import updates_task_format_log

logger = get_task_logger(__name__)


@shared_task(name='updates.email_send', ignore_result=True)
def email_send_task(email):
    logger.info('sending email')
    send_mail(
        f"User {email} deleted his update",
        "Delete request for measures update",
        email,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )


@shared_task(name='updates.image_resize')
def image_resize_task(path, width, height, by_wdith=False):
    return image_resize(path=path, width=width, height=height, by_wdith=by_wdith)


@shared_task(name='updates.delete_profile_updates', ignore_result=True)
def delete_profile_updates():
    count, obj = delete_all_profile_updates()
    logger.info(updates_task_format_log(
        name='profile', count=count, obj=obj))


@shared_task(name='updates.delete_measures_updates', ignore_result=True)
def delete_measures_updates():
    count, obj = delete_all_measures_updates()
    logger.info(updates_task_format_log(
        name='measures', count=count, obj=obj))


@shared_task(name='updates.delete_gallery_updates', ignore_result=True)
def delete_gallery_updates():
    count, obj = delete_all_gallery_updates()
    logger.info(updates_task_format_log(
        name='gallery', count=count, obj=obj))


@shared_task(name='updates.delete_profile_picture_updates', ignore_result=True)
def delete_profile_picture_updates():
    count, obj = delete_all_profile_picture_updates()
    logger.info(updates_task_format_log(
        name='profile_picture', count=count, obj=obj))


@shared_task(name='updates.delete_cover_picture_updates', ignore_result=True)
def delete_cover_picture_updates():
    count, obj = delete_all_cover_picture_updates()
    logger.info(updates_task_format_log(
        name='cover_picture', count=count, obj=obj))


@shared_task(name='updates.delete_updates', ignore_result=True)
def delete_updates_task():
    # Execute daily at midnight.
    # tasks will run in parallel
    lazy_group = group([
        delete_profile_updates.s(),
        delete_measures_updates.s(),
        delete_gallery_updates.s(),
        delete_profile_picture_updates.s(),
        delete_cover_picture_updates.s()
    ])
    lazy_group()
