
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name']
        read_only_fields = ['id']

class UserUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
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