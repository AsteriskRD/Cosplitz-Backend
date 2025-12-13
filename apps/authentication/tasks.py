from celery import shared_task
from django.contrib.auth import get_user_model

from apps.common.utils import simple_mail, send_otp_code_brevo, send_welcome_mail_brevo, send_user_mail
from apps.splits.models import Splits
from apps.users.models import Notification

User = get_user_model()


# @shared_task
# def send_otp_code_mail(user_email, otp_code):
#
#     context = {
#         'subject': 'Verification Otp',
#         'to_email': user_email,
#         'content': {
#             'otp': otp_code
#         }
#     }
#     template = 'emails/login_email.html'
#     success = simple_mail(html_template=template, context=context)
@shared_task
def send_otp_code_mail(user_email, otp_code):

    context = {
        'subject': 'Verification Otp',
        'to_email': user_email,
        'html_contents' : {
            'otp_code': otp_code,
            'expiry_minutes': 10,
        }
    }
    template = 'emails/otp_email.html'
    send_user_mail(template, context)

@shared_task()
def send_welcome_mail(content):
    template = 'emails/welcome_mail.html'
    context = {
        'subject': 'Welcome Mail',
        'to_email': content.get('to_email'),
        'html_contents' : {
            'full_name' : content.get('full_name')
        }
    }
    send_user_mail(template, context)

@shared_task
def send_split_creation_mail(user_id, splits_id):
    user = User.objects.get(id=user_id)
    splits = Splits.objects.get(id=splits_id)
    context = {
        'subject': 'Splitz Creation',
        'to_email': user.email,
        # 'to_email': 'omotosoeniola2@gmail.com',
        'content': {
            'name': splits.title,
            'creator' : user.first_name + ' ' + user.last_name
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
        message=f'Your split "{splits.title}" has been created.',
        is_read=False
    )

    # Send email
    send_split_creation_mail(user.id, splits.id)