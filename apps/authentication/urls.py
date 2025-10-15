from apps.authentication.views import UserRegisterView
from apps.users.urls import path

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
]