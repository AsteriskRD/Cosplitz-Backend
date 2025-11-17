
from rest_framework import serializers

from .models import Splits

class SplitzSerializer(serializers.ModelSerializer):
    """Serializers for splitz"""
    class Meta:
        model = Splits
        fields = '__all__'
        read_only_fields = ['id']


