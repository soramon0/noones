from celery import shared_task
from celery.utils.log import get_task_logger

# from accounts.services import confirmation_email_send

# logger = get_task_logger(__name__)


# @shared_task()
# def confirmation_email_send_task(scheme, domain, user):
#     logger.info('sending confirmation email')
#     return confirmation_email_send(scheme=scheme, domain=domain, user=user)
