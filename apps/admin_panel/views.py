from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from apps.kyc.models import KYCVerification
from apps.admin_panel.permissions import IsAdminUser
from django.core.mail import send_mail



from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def admin_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    if not email or not password:
        return Response({"message": "Email and password required"}, status=400)

    # authenticate user
    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response({"message": "Invalid credentials"}, status=401)

    if not user.is_staff:
        return Response({"message": "Not allowed. This user is not admin."}, status=403)

    # generate tokens
    refresh = RefreshToken.for_user(user)

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }, status=200)



#  List all KYC submissions
@api_view(["GET"])
@permission_classes([IsAdminUser])
def list_kyc(request):
    kycs = KYCVerification.objects.all().order_by("-created_at")

    data = [
        {
            "id": kyc.id,
            "user": kyc.user.email,
            "first_name": kyc.first_name,
            "last_name": kyc.last_name,
            "nationality": kyc.nationality,
            "email": kyc.email,
            "document_type": kyc.document_type,
            "is_verified": kyc.is_verified,
            "verified_by_admin": kyc.verified_by_admin,
            "created_at": kyc.created_at,
        }
        for kyc in kycs
    ]

    return Response(data, status=status.HTTP_200_OK)


#  Get details of one KYC
@api_view(["GET"])
@permission_classes([IsAdminUser])
def kyc_detail(request, kyc_id):
    try:
        kyc = KYCVerification.objects.get(id=kyc_id)
    except KYCVerification.DoesNotExist:
        return Response({"message": "KYC not found"}, status=status.HTTP_404_NOT_FOUND)

    data = {
        "id": kyc.id,
        "user": kyc.user.email,
        "first_name": kyc.first_name,
        "last_name": kyc.last_name,
        "nationality": kyc.nationality,
        "email": kyc.email,
        "city": kyc.city,
        "district": kyc.district,
        "full_address": kyc.full_address,
        "document_type": kyc.document_type,
        "is_verified": kyc.is_verified,
        "verified_by_admin": kyc.verified_by_admin,
        "created_at": kyc.created_at,
        "document_front": request.build_absolute_uri(kyc.document_front.url) if kyc.document_front else None,
        "document_back": request.build_absolute_uri(kyc.document_back.url) if kyc.document_back else None,
    }

    return Response(data, status=status.HTTP_200_OK)


#  Approve KYC
@api_view(["POST"])
@permission_classes([IsAdminUser])
def approve_kyc(request, kyc_id):
    try:
        kyc = KYCVerification.objects.get(id=kyc_id)
    except KYCVerification.DoesNotExist:
        return Response({"message": "KYC not found"}, status=status.HTTP_404_NOT_FOUND)

    kyc.is_verified = True
    kyc.verified_by_admin = True
    kyc.save()

    # Send email
    send_mail(
        subject="KYC Verification Approved",
        message=f"Hello {kyc.first_name},Your KYC has been approved.",
        from_email="omotosoeniola191@gmail.com",
        recipient_list=[kyc.email],
        fail_silently=True,
    )


    return Response({"message": "KYC approved successfully"}, status=status.HTTP_200_OK)


#  Reject KYC
@api_view(["POST"])
@permission_classes([IsAdminUser])
def reject_kyc(request, kyc_id):
    try:
        kyc = KYCVerification.objects.get(id=kyc_id)
    except KYCVerification.DoesNotExist:
        return Response({"message": "KYC not found"}, status=status.HTTP_404_NOT_FOUND)

    kyc.is_verified = False
    kyc.verified_by_admin = True
    kyc.save()

    send_mail(
        subject="KYC Verification Failed",
        message=f"Hello {kyc.first_name},Your KYC submission was rejected.",
        from_email="omotosoeniola191@gmail.com",
        recipient_list=[kyc.email],
        fail_silently=True,
    )

    return Response({"message": "KYC rejected"}, status=status.HTTP_200_OK)
