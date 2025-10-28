from django.http import Http404
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status

from apps.users.selector import user_get
from apps.users.serializers import UserSerializer, UserUpdateSerializer
from apps.common.utils import simple_mail, generate_otp
from apps.users.service import user_create, user_update


# Create your views here.
class UserDetailsAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        if user is None:
            raise Http404

        serializer = UserSerializer(user)
        # serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
class UserUpdateApi(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, user_id):
        serializer = UserUpdateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = user_get(user_id)

        if user is None:
            raise Http404

        user = user_update(user=user, data=serializer.validated_data)

        data = UserSerializer(user).data

        return Response(data)



