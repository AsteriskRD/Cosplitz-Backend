from django.urls import path
from . import views

urlpatterns = [
    # KYC Endpoints
    path("submit/", views.kyc_submit, name="kyc_submit"),
    path("details/", views.kyc_details, name="kyc_details"),
]
