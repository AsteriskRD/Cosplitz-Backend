from django.urls import path

from .views import UserUpdateApi, UserCreateView, UserDetailsAPI,KYCSubmitAPI,KYCDetailAPI

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="create"),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name="update"),
    path('<int:user_id>/', UserDetailsAPI.as_view(), name="details"),

    # --- KYC endpoints ---
    path("kyc/submit/", KYCSubmitAPI.as_view(), name="kyc_submit"),
    path("kyc/details/", KYCDetailAPI.as_view(), name="kyc_details"),
]