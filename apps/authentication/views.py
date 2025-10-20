from django.contrib.auth import authenticate, get_user_model
from django.utils.autoreload import raise_last_exception
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authentication.selector import user_get_login_data, get_user_token_for_user
from apps.users.service import user_create
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

        user = authenticate(
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

        return Response({
            "message" : "Login successful",
            "token" : str(jwt_token.access_token),
            "refresh_token" : str(jwt_token),
            "data" : data,
        }, status=status.HTTP_200_OK)
