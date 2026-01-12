from rest_framework import mixins, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Splits
from .serializer import SplitsSerializer
from .services import join_split, fetch_splits_joined_by_user
from ..authentication.tasks import send_split_notifications

from ..common.utils.response import CustomJSONRenderer


class SplitsViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = SplitsSerializer
    queryset = Splits.objects.all()
    permission_classes  = [IsAuthenticated]
    renderer_classes = [CustomJSONRenderer]
    # authentication_classes = []
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


class JoinSplitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, split_id):
        try :
            join_split(split_id = split_id, user =request.user)

            return Response({
                'status': 'success',
                'message': 'Successfully joined split',
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e),
            })


class UserJoinedSplitsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print('working')
        splits = fetch_splits_joined_by_user(user=request.user)
        serializer = SplitsSerializer(splits, many=True)

        return Response({
            'data': serializer.data
        })


