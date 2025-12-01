from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.admin_login),
    path("kyc/", views.list_kyc, name="admin_list_kyc"),
    path("kyc/<int:kyc_id>/", views.kyc_detail, name="admin_kyc_detail"),
    path("kyc/<int:kyc_id>/approve/", views.approve_kyc, name="admin_approve_kyc"),
    path("kyc/<int:kyc_id>/reject/", views.reject_kyc, name="admin_reject_kyc"),
]
