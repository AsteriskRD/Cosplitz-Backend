from rest_framework import serializers

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
