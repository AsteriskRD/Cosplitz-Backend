from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserUpdateApi, UserDetailsAPI, KYCSubmitAPI, KYCDetailAPI, NotificationViewSet



# router = DefaultRouter()
#
# router.register('notifications', NotificationViewSet)
urlpatterns = [
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name="update"),
    path('info', UserDetailsAPI.as_view(), name="details"),

    

    # --- Notifiaction endpoints-----


]
