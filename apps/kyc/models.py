from django.db import models
from apps.users.models import User

class KYCVerification(models.Model):
    #Stores KYC details for each user Each user can only have one KYC record. Verification is manual (by admin).

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
    document_front = models.FileField(upload_to="kyc_documents/", null=True, blank=True)
    document_back = models.FileField(upload_to="kyc_documents/", null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.document_type}"

