from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  serializers

from apps.users.selector import user_get
from apps.users.serializers import  OutputSerializer,KYCSerializer
from apps.users.service import user_create


from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import KYCVerification



# Create your views here.
class UserCreateView(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        username = serializers.CharField()
        password = serializers.CharField()
        address = serializers.CharField()
        city = serializers.CharField()
        state = serializers.CharField()
        zipcode = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(**serializer.validated_data)

        data = OutputSerializer(data=request.data)

        return Response(data)

class UserDetailsAPI(APIView):
    def get(self, request, user_id):
        # user = user_get(user_id)
        return Response(user_id)
        # if user is None:
        #     raise Http404
        #
        # data = OutputSerializer(data=request.data)
        # return Response(data)

class UserUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        username = serializers.CharField(required=False)
        password = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        city = serializers.CharField(required=False)
        state = serializers.CharField(required=False)
        zipcode = serializers.CharField(required=False)

    def patch(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        user = user_get(user_id)
        if user is None:
            raise Http404

        user = user


#KYC Verification Views Handles API endpoints for creating and viewing KYC verification records.
class KYCSubmitAPI(APIView):
    
    #Allows a logged-in user to submit their KYC verification details. The record is created and stored for admin to review later.
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if user already has a KYC record
        if hasattr(request.user, "kyc"):
            return Response(
                {"message": "You have already submitted your KYC."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = KYCSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "KYC submitted successfully. Await admin verification."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KYCDetailAPI(APIView):
    #Retrieve the logged-in user's KYC details.

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            kyc = KYCVerification.objects.get(user=request.user)
            serializer = KYCSerializer(kyc)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KYCVerification.DoesNotExist:
            return Response(
                {"message": "No KYC record found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )


class KYCDetailAPI(APIView):
    
    #Retrieve the logged-in user's KYC details and status.
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            kyc = KYCVerification.objects.get(user=request.user)
            serializer = KYCSerializer(kyc)

            # Determine KYC status message
            if kyc.is_verified and kyc.verified_by_admin:
                status_message = " KYC verification successful."
            elif not kyc.is_verified and kyc.verified_by_admin:
                status_message = " KYC verification failed."
            else:
                status_message = " KYC verification pending. Await admin approval."

            return Response(
                {
                    "status": status_message,
                    "kyc_details": serializer.data
                },
                status=status.HTTP_200_OK
            )

        except KYCVerification.DoesNotExist:
            return Response(
                {"message": "No KYC record found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )
