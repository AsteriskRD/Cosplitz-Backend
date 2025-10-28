from django.urls import path

from .views import UserDetailsAPI, UserUpdateApi

urlpatterns = [

    path('info', UserDetailsAPI.as_view(), name="details"),
    path('<int:user_id>/update/', UserUpdateApi.as_view(), name="update"),

]