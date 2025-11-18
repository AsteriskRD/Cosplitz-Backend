from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.splits.views import SplitsViewSet

router = DefaultRouter()

router.register('', SplitsViewSet)
urlpatterns = [
    path('', include(router.urls)),

]
