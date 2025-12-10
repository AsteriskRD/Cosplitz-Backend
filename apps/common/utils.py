import random
from datetime import timedelta
from typing import List
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, get_connection
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import logging

from apps.common.services import send_email_via_brevo_api
from apps.users.models import EmailOtp

logger = logging.getLogger(__name__)


def get_object(model_or_queryset, **kwargs):
    """
    Reuse get_object_or_404 since the implementation supports both Model && queryset.
    Catch Http404 & return None
    """
    try:
        return get_object_or_404(model_or_queryset, **kwargs)
    except Http404:
        return None


def simple_mail(html_template, context):
    from_email : str = getattr(settings, "DEFAULT_FROM_EMAIL", 'omotosoeniola191@gmail.com')
    subject : str = context.get('subject')
    to_email : str = context.get('to_email')

    if not to_email :
        raise ValueError("Recipient email not provided")
    if not subject:
        raise ValueError("Email subject is required")

    if isinstance(to_email, str):
        to_email : List = [to_email]

    try:
        html_message : str = render_to_string(html_template, context)
        plain_message = strip_tags(html_message)

        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            fail_silently=False,
            timeout=30,
        )

        # Open connection explicitly
        connection.open()

        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=from_email,
            to=to_email,
            connection=connection
        )

        message.content_subtype = "html"
        message.send(fail_silently=False)

        logger.info(f"Email sent successfully to {', '.join(to_email)} - Subject: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {', '.join(to_email)} - Subject: {subject}")
        logger.exception(e)
        # Re-raise for Celery to retry
        return False
    # finally:
    #     # Always close connection
    #     if connection:
    #         try:
    #             connection.close()
    #         except Exception as e:
    #             logger.warning(f"Error closing SMTP connection: {e}")


def generate_otp(user):
    otp_code : str = str(random.randint(100000, 999999))
    expiry_time = timezone.now() + timedelta(minutes=10)

    EmailOtp.objects.update_or_create(
        user=user,
        defaults={
            'otp_code':otp_code,
            'expiry_at':expiry_time,
        }
    )

    return otp_code


def send_otp_code_mail(self, email, otp_code):
    html_content = f"""
    <html>
        <body>
            <h2>Your OTP Code</h2>
            <p>Your verification code is: <strong>{otp_code}</strong></p>
            <p>This code will expire in 10 minutes.</p>
        </body>
    </html>
    """

    try:
        success = send_email_via_brevo_api(
            to_email=email,
            subject="Verification OTP",
            html_content=html_content
        )

        if success:
            logger.info(f"OTP sent successfully to {email}")
            return True
        else:
            logger.error(f"Failed to send OTP to {email}")
            return False

    except Exception as e:
        logger.error(f"Error sending OTP to {email}: {e}")
        raise self.retry(exc=e, countdown=60)

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']

        if response.status_code >= 400:
            custom_response = {
                'status': 'error',
                'message': data.get('detail', 'An error occurred'),
                'errors': data
            }
        else:
            custom_response = {
                'status': 'success',
                'data': data
            }

        return super().render(custom_response, accepted_media_type, renderer_context)
