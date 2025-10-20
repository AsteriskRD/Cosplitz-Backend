from apps.authentication.views import UserRegisterView, UserLoginView
from apps.users.urls import path

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
]