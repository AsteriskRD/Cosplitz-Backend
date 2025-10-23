from rest_framework import serializers
from .models import KYCVerification

class CreateInputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zipcode = serializers.CharField()

class OutputSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()



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
        read_only_fields = ["is_verified", "verified_by_admin", "created_at", "user"]
