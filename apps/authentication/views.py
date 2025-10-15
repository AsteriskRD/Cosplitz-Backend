from django.contrib.auth import authenticate
from django.utils.autoreload import raise_last_exception
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from apps.authentication.selector import user_get_login_data, get_user_token_for_user
from apps.users.service import user_create
from apps.users.serializers import UserSerializer

class UserRegisterView(APIView):
    """Register a new user"""
    permission_classes = [AllowAny]

    @extend_schema(
        request={},
        responses={
            201: UserSerializer,
            400: OpenApiResponse(
                # response=ErrorResponseSerializer,
                description='Validation error or user already exists'
            ),
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
            "user" : UserSerializer(user).data,
        })

class UserLoginView(APIView):
    """Login a user"""

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=True)
        password = serializers.CharField(required=True)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response({
                'message' : "User credentials invalid",
            }, status=status.HTTP_400_BAD_REQUEST)

        data = user_get_login_data(user=user)
        jwt_token = get_user_token_for_user(user=user)

        return Response({
            "message" : "Login successful",
            "token" : jwt_token.access_token,
            "refresh_token" : jwt_token.refresh_token,
            "data" : data,
        }, status=status.HTTP_200_OK)
