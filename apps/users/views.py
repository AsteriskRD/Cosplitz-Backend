from django.http import Http404
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import  serializers

from apps.users.selector import user_get
from apps.users.serializers import  OutputSerializer
from apps.users.service import user_create


# Create your views here.
class UserCreateView(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        username = serializers.CharField()
        password = serializers.CharField()
        address = serializers.CharField()
        city = serializers.CharField()
        state = serializers.CharField()
        zipcode = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = user_create(**serializer.validated_data)

        data = OutputSerializer(data=request.data)

        return Response(data)

class UserDetailsAPI(APIView):
    def get(self, request, user_id):
        # user = user_get(user_id)
        return Response(user_id)
        # if user is None:
        #     raise Http404
        #
        # data = OutputSerializer(data=request.data)
        # return Response(data)

class UserUpdateApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField(required=False)
        username = serializers.CharField(required=False)
        password = serializers.CharField(required=False)
        address = serializers.CharField(required=False)
        city = serializers.CharField(required=False)
        state = serializers.CharField(required=False)
        zipcode = serializers.CharField(required=False)

    def patch(self, request, user_id):
        serializer = self.InputSerializer(data=request.data)
        user = user_get(user_id)
        if user is None:
            raise Http404

        user = user
