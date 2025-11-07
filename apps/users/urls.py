from django.urls import path

from .views import UserDetailsAPI, UserUpdateApi

urlpatterns = [

    path('info', UserDetailsAPI.as_view(), name="details"),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name="update"),

    # --- KYC endpoints ---
    path("kyc/submit/", KYCSubmitAPI.as_view(), name="kyc_submit"),
    path("kyc/details/", KYCDetailAPI.as_view(), name="kyc_details"),

]
