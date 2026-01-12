
from rest_framework import serializers

from apps.splits.models import Splits

class SplitsSerializer(serializers.ModelSerializer):
    """Serializers for splits"""
    class Meta:
        model = Splits
        fields = '__all__'
        read_only_fields = ['id', 'user']

        def update(self, instance, validated_data):
            # Image upload is handled automatically
            instance.avatar = validated_data.get('image_url', instance.avatar)
            instance.save()
            return instance

