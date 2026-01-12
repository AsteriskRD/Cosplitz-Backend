from rest_framework import serializers


class CreateVirtualAccountSerializer(serializers.Serializer):
    """Serializer for creating virtual account"""
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    currency = serializers.ChoiceField(choices=['NGN', 'USD', 'GHS'], default='NGN')
    account_type = serializers.ChoiceField(choices=['dynamic', 'static'], default='dynamic')
    expiry = serializers.IntegerField(default=60, min_value=1)
    narration = serializers.CharField(max_length=255, required=False)
