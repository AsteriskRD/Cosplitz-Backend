from celery import shared_task
from django.contrib.auth import get_user_model

from apps.common.utils import simple_mail, generate_otp
from apps.splitz.models import Splits
from apps.users.models import Notification

User = get_user_model()


@shared_task
def send_otp_code_mail(user_email, otp_code):

    context = {
        'subject': 'Verification Otp',
        'to_email': user_email,
        # 'to_email': 'omotosoeniola2@gmail.com',
        'content': {
            'otp': otp_code
        }
    }
    template = 'emails/login_email.html'
    success = simple_mail(html_template=template, context=context)

@shared_task
def send_split_creation_mail(user_id, splits_id):
    user = User.objects.get(id=user_id)
    splits = Splits.objects.get(id=splits_id)
    context = {
        'subject': 'Splitz Creation',
        'to_email': user.email,
        # 'to_email': 'omotosoeniola2@gmail.com',
        'content': {
            'name': splits.name,
            'creator' : user.name
        }
    }

    template = 'emails/split_creation_email.html'
    simple_mail(html_template=template, context=context)


@shared_task
def send_split_notifications(user_id, splits_id):
    user = User.objects.get(id=user_id)
    splits = Splits.objects.get(id=splits_id)

    # Create inbox notification
    notification = Notification.objects.create(
        user=user,
        notification_type='split_created',
        title='Split Created Successfully',
        message=f'Your split "{splits.name}" has been created.',
        related_object_id=splits.id,
        related_object_type='split',
        is_read=False
    )

    # Send email
    send_split_creation_mail(user.id, splits.id)