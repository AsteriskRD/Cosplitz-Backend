from celery import shared_task

from apps.common.utils import simple_mail, generate_otp


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