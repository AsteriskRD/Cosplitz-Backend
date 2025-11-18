from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .models import KYCVerification



@api_view(["POST"])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def kyc_submit(request):
    user = request.user

    # Prevent duplicate submission
    if hasattr(user, "kyc"):
        return Response({"message": "You have already submitted your KYC."}, status=400)

    # File upload
    document_front = request.FILES.get("document_front")
    document_back = request.FILES.get("document_back")
    if not document_front or not document_back:
        return Response({"message": "Document file is required."}, status=400)

    # Required fields
    required_fields = [
        "first_name", "last_name", "nationality", "email",
        "city", "district", "full_address", "document_type"
    ]

    for field in required_fields:
        if field not in request.data:
            return Response({"message": f"Missing field: {field}"}, status=400)

    # Create KYC record
    kyc = KYCVerification.objects.create(
        user=user,
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        nationality=request.data["nationality"],
        email=request.data["email"],
        city=request.data["city"],
        district=request.data["district"],
        full_address=request.data["full_address"],
        document_type=request.data["document_type"],
        document_front=document_front,
        document_back=document_back
    )

    return Response({"message": "KYC submitted successfully. Await admin verification."}, status=201)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kyc_details(request):
    try:
        kyc = KYCVerification.objects.get(user=request.user)
    except KYCVerification.DoesNotExist:
        return Response({"message": "No KYC record found for this user."}, status=404)

    if kyc.is_verified and kyc.verified_by_admin:
        status_message = "KYC verification successful."
    elif not kyc.is_verified and kyc.verified_by_admin:
        status_message = "KYC verification failed."
    else:
        status_message = "KYC verification pending. Await admin approval."

    return Response({
        "status": status_message,
        "kyc_details": {
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
        }
    }, status=200)
