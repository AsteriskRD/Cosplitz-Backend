from django.contrib import admin
from .models import KYCVerification

# Register your models here.

#KYC admin management for manual verification.

@admin.register(KYCVerification)
class KYCVerificationAdmin(admin.ModelAdmin):
    #Admin panel for KYC records. Allows viewing, filtering, and verifying users manually.
    list_display = (
        "user",
        "first_name",
        "last_name",
        "email",
        "document_type",
        "is_verified",
        "verified_by_admin",
        "created_at",
    )

    search_fields = ("first_name", "last_name", "email", "nationality")
    list_filter = ("is_verified", "verified_by_admin", "document_type")
    readonly_fields = ("created_at",)
    actions = ["verify_selected", "reject_selected"]

    def verify_selected(self, request, queryset):
        #Manually verify selected KYC records from admin dashboard.
        updated = queryset.update(is_verified=True, verified_by_admin=True)
        self.message_user(request, f"{updated} user(s) verified successfully!")

    verify_selected.short_description = " Verify selected KYC users"

    def reject_selected(self, request, queryset):
        #Mark selected KYC users as failed verification.
        updated = queryset.update(is_verified=False, verified_by_admin=False)
        self.message_user(request, f"{updated} user(s) rejected.")

    reject_selected.short_description = " Reject selected KYC users"

