import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager as BUM
from django.db import models
from django.utils import timezone

from apps.common.models import BaseModel


class BaseUserManager(BUM):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(
            email.lower()), **extra_fields)
        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.full_clean()
        user.save(using=self._db)

        return user

    # def create_superuser(self, email, password=None):
    #     user = self.create_user(email=email, password=password)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True)
    first_name = models.CharField(verbose_name="first name", max_length=255)
    last_name = models.CharField(verbose_name="last name", max_length=255)
    username = models.CharField(
        verbose_name="username", max_length=255, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def is_staff(self):
        return self.is_admin


def get_otp_expiry_time():
    return timezone.now() + timedelta(minutes=5)


class EmailOtp(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    # expiry_at = models.DateTimeField(default=get_otp_expiry_time)
    expiry_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expiry_at

    def __str__(self):
        return f"OTP for {self.user.email}"


class KYCVerification(models.Model):
    # Stores KYC details for each user Each user can only have one KYC record. Verification is manual (by admin).

    DOCUMENT_CHOICES = [
        ("national_id", "National ID Card"),
        ("drivers_license", "Driver's License"),
        ("passport", "International Passport"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="kyc",
        help_text="The user who submitted this KYC record.",
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    full_address = models.TextField()
    document_type = models.CharField(max_length=50, choices=DOCUMENT_CHOICES)
    document_file = models.FileField(upload_to="kyc_documents/")
    is_verified = models.BooleanField(default=False)
    verified_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}"
