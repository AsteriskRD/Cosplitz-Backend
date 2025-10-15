from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User

def user_get_login_data(*, user : User | AbstractBaseUser):
    return {
        "id" : user.id,
        "email" : user.email,
        "username" : user.username,
        "is_active" : user.is_active
    }

def get_user_token_for_user(user : User | AbstractBaseUser):
    if not user.is_active:
        raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        "access_token" : str(refresh.access_token),
        "refresh_token" : str(refresh)
    }