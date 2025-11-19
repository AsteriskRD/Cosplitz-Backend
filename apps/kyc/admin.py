from django.contrib import admin
from .models import KYCVerification
from django.core.mail import send_mail

# Register your models here.
@admin.register(KYCVerification)
class KYCVerificationAdmin(admin.ModelAdmin):

    #Admin panel for KYC records. Allows viewing, filtering, verifying, and rejecting users manually.

    list_display = (
        "user",
        "first_name",
        "last_name",
        "email",
        "nationality",
        "city",
        "district",
        "full_address",
        "document_type",
        "document_front",
        "document_back",
        "is_verified",
        "verified_by_admin",
        "created_at",
    )

    search_fields = ("first_name", "last_name", "email", "nationality")
    list_filter = ("is_verified", "verified_by_admin", "document_type")
    readonly_fields = ("created_at",)
    fields = (
        "user",
        "first_name",
        "last_name",
        "email",
        "nationality",
        "city",
        "district",
        "full_address",
        "document_type",
        "document_front",
        "document_back",
        "is_verified",
        "verified_by_admin",
        "created_at",
    )
    actions = ["verify_selected", "reject_selected"]

    def verify_selected(self, request, queryset):
        """
        Manually verify selected KYC records from the admin dashboard.
        Also send email notification to users after approval.
        """
        for kyc in queryset:
            kyc.is_verified = True
            kyc.verified_by_admin = True
            kyc.save()

            # Send approval email
            send_mail(
                subject="KYC Verification Approved",
                message=f"Hello {kyc.first_name},Your KYC verification has been approved successfully.\n\nThank you!",
                from_email="omotosoeniola191@gmail.com",
                recipient_list=[kyc.email],
                fail_silently=True,
            )

        self.message_user(request, f"{queryset.count()} user(s) verified successfully!")

    verify_selected.short_description = " Verify selected KYC users"

    def reject_selected(self, request, queryset):
    
        #Mark selected KYC users as failed verification and send rejection email.

        for kyc in queryset:
            kyc.is_verified = False
            kyc.verified_by_admin = True  # Important: Set to True so system knows admin reviewed it
            kyc.save()

            # Send rejection email
            send_mail(
                subject="KYC Verification Rejected",
                message=f"Hello {kyc.first_name},Unfortunately, your KYC verification was not successful.\nPlease review your submission and try again.\n\nThank you!",
                from_email="omotosoeniola191@gmail.com",
                recipient_list=[kyc.email],
                fail_silently=True,
            )

        self.message_user(request, f"{queryset.count()} user(s) rejected.")

    reject_selected.short_description = " Reject selected KYC users"
