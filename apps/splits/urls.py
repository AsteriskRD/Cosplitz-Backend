from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.splits.views import SplitsViewSet, JoinSplitView, UserJoinedSplitsView

router = DefaultRouter()

router.register('', SplitsViewSet)
urlpatterns = [
    path('my_splits/', UserJoinedSplitsView.as_view(), name='user-joined-splits'),
    path('', include(router.urls)),
    path('<int:split_id>/join_splits/', JoinSplitView.as_view(), name='splits'),

]
