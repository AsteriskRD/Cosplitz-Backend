from django.urls import path

from .views import UserUpdateApi, UserDetailsAPI

urlpatterns = [

    path('<int:user_id>/update/', UserUpdateApi.as_view(), name="update"),
    path('<int:user_id>/', UserDetailsAPI.as_view(), name="details")
]