from django.conf import settings
from django.db import models

from apps.authentication.tasks import User


class UserAccountDetails(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reference = models.CharField(max_length=120, blank=True)
    customer_id= models.CharField(max_length=120)
    account_type = models.CharField(max_length=120, default='dynamic')
    currency = models.CharField(max_length=10, default='NGN')
    idempotency_key = models.CharField(max_length=120, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.customer_id}"