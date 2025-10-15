
from django.contrib.auth import get_user_model
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    class Meta:
        model = get_user_model()
        fields = ['email', 'password',
                  'first_name', 'last_name', 'username']
        extra_kwargs = {'password': {'write_only': True}}

class OutputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
