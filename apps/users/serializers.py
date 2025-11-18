
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import KYCVerification, Notification


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'nationality', 'first_name', 'last_name', 'username']
        read_only_fields = ['id']


class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    nationality = serializers.CharField(required=False)
    password = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    city = serializers.CharField(required=False)
    state = serializers.CharField(required=False)
    zipcode = serializers.CharField(required=False)


class UserRegisterResponseSerializer(serializers.Serializer):
    """Full response wrapper for user registration"""
    message = serializers.CharField()
    user = OutputSerializer()


class ErrorResponseSerializer(serializers.Serializer):
    """Error response schema"""
    error = serializers.CharField()
    details = serializers.CharField(required=False)


class NotificationSerializers(serializers.ModelSerializer):
    """Notification schema"""
    class Meta:
        model = Notification
        fields = '__all__'
        read_only_fields = ['id', 'message', 'notification_type', 'user_id']

# Serializer for KYC verification data. Used to validate incoming JSON data and return clean API responses.
class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCVerification
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "nationality",
            "email",
            "city",
            "district",
            "full_address",
            "document_type",
            "document_file",
            "is_verified",
            "verified_by_admin",
            "created_at",
        ]
        read_only_fields = ["is_verified",
                            "verified_by_admin", "created_at", "user"]
