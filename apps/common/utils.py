import random
from datetime import timedelta
from typing import List
from django.conf import settings
from django.core.mail import send_mail, EmailMessage
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

from rest_framework.response import Response
import logging

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

        message = EmailMessage(
            subject=subject,
            body=html_message,
            from_email=from_email,
            to=to_email
        )

        message.content_subtype = "html"
        message.send(fail_silently=False)

        logger.info(f"Email sent successfully to {', '.join(to_email)} - Subject: {subject}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {', '.join(to_email)} - Subject: {subject}")
        logger.exception(e)
        return False

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