from apps.authentication.views import UserRegisterView, UserLoginView, SendUserOtp, VerifyOtp
from apps.users.urls import path

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),

    path('otp/<int:user_id>/', SendUserOtp.as_view(), name="send_otp"),
    path('verify_otp', VerifyOtp.as_view(), name="verify_otp")

]