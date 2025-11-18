from pickle import FALSE

from django.http import Http404
from django.utils import timezone

from django.shortcuts import render
from django.template.context_processors import request
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status, mixins, viewsets

from apps.users.selector import user_get
from apps.users.serializers import UserSerializer, UserUpdateSerializer, NotificationSerializers
from apps.common.utils import simple_mail, generate_otp
from apps.users.service import user_create, user_update


from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import KYCVerification, Notification


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


class NotificationViewSet(mixins.ListModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers
    permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=False, methods=["post"])
    def mark_all_read(self, request):
        """Mark all notifications as read."""
        count = self.get_queryset().filter(is_read=False).update(is_read=True, read_at=timezone.now())

        return Response({'message' : 'Successfully marked as read' })


    @action(detail=True, methods=["post"])
    def mark_read(self,request, pk=None):
        """Mark specific notification as read."""
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()

        return Response({'status': 'marked as read'})
