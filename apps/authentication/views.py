from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.selector import user_get_login_data, get_user_token_for_user
from apps.common.utils import simple_mail, generate_otp
from apps.users.models import EmailOtp
from apps.users.service import user_create
from apps.users.selector import user_get
from apps.users.serializers import UserSerializer, OutputSerializer, ErrorResponseSerializer, \
    UserRegisterResponseSerializer


class UserRegisterView(APIView):
    """Register a new user"""
    permission_classes = [AllowAny]

    @extend_schema(
        request=UserSerializer,
        responses={
            201: UserRegisterResponseSerializer,  # Full response with message + user
            400: ErrorResponseSerializer,  # Proper error schema
        },
        description="Create a new user account with email and password",
        tags=['Authentication']
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = user_create(**serializer.validated_data)
            # context = {
            #     'subject': 'Welcome to Our Platform',
            #     'to_email': 'omotosoeniola2@gmail.com',
            #     'content': {
            #         'otp': otp_code
            #     }
            # }
            # template = 'emails/login_email.html'
            # success = simple_mail(html_template=template, context=context)
            # if not success:
            #     return Response({'error': "message not sent"})
        except Exception as e:
            return Response({
                "error" : "Failed to create user", "details" :  str(e),
            },status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message" : "User created successfully",
            "user" : OutputSerializer(user).data,
        }, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    """Login a user"""
    permission_classes = [AllowAny]

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)

    @extend_schema(
        request=InputSerializer,
    )

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        authenticate(
            request, username=serializer.validated_data['email'],
            password=serializer.validated_data['password'])

        user = get_user_model().objects.get(email=serializer.validated_data['email'])

        print(f"user: {user}")

        if user is None:
            return Response({
                'message' : "User credentials invalid",
            }, status=status.HTTP_401_UNAUTHORIZED)

        data = user_get_login_data(user=user)
        jwt_token = refresh = RefreshToken.for_user(user)
        otp_code = generate_otp(user)

        return Response({
            "message" : "Login successful",
            "token" : str(jwt_token.access_token),
            "refresh_token" : str(jwt_token),
            "data" : data,
        }, status=status.HTTP_200_OK)



class SendUserOtp(APIView):
    """Send Verification code"""
    def get(self, request, user_id):
        user = user_get(user_id)

        if user is None:
            return Response({
                'message': 'User does not exist',
                'status_code': status.HTTP_404_NOT_FOUND
            }, status=status.HTTP_404_NOT_FOUND)

        otp_code = generate_otp(user)
        context = {
            'subject': 'Verification Otp',
            'to_email': user.email,
            'content': {
                'otp': otp_code
            }
        }
        template = 'emails/login_email.html'
        success = simple_mail(html_template=template, context=context)
        if not success :
            return Response({'error' : "message not sent"})
        return Response({
            'message': 'OTP sent',
        },status=status.HTTP_200_OK)


class VerifyOtp(APIView):
    class InputSerializer(serializers.Serializer):
        otp = serializers.CharField(required=True)
        email = serializers.EmailField(required=True)
    def post(self, request):
        serializer = self.InputSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        #confrim OTP get user otp from the database
        try:
            email_otp = EmailOtp.objects.get(user__email=data['email'])
        except EmailOtp.DoesNotExist:
            return Response({
                "message": "No OTP Found for user",
            },status=status.HTTP_400_BAD_REQUEST)

        # Validate OTP
        if email_otp.otp_code != data['otp']:
            return Response({
                'message' : "OTP Expired",
                'status' : 400
            }, status=status.HTTP_401_UNAUTHORIZED)
        #check expiration
        if email_otp.expiry_at < timezone.now():
            return Response({
                "message" : "OTP expired",
            },status=status.HTTP_400_BAD_REQUEST)

        # Mark User as verified
        user = email_otp.user
        user.is_active= True
        user.save()

        #deleete OTP
        email_otp.delete()
        return Response({
            "message" : "OTP verified",
        }, status=status.HTTP_200_OK)

