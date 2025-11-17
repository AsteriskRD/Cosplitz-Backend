from rest_framework import mixins, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Splits
from .serializer import SplitzSerializer
from ..authentication.task import send_split_creation_mail, send_split_notifications
from rest_framework import serializers


class SplitsViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = SplitzSerializer
    queryset = Splits.objects.all()
    permission_classes  = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    ordering_fields = ['created_at']
    # pagination_class = Standard

    def perform_create(self, serializer):
        user = self.request.user
        splits = serializer.save(user=user)
        #Extra logic
        # Send all notifications asynchronously
        send_split_notifications.delay(user.id, splits.id)


    # def perform_update(self, serializer):
    #     user = self.request.user
    #     splits = serializer.
    #
    #     #stor inbox notification

