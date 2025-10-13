from typing import Optional

from django.db import transaction

from .models import User

@transaction.atomic
def user_create(*, email:str, password:Optional[str] =None, **extra_fields ) -> User:
    user = User.objects.create_user(email=email, password=password, **extra_fields)
    return user

# @transaction.atomic
# def user_update(*, user:User, data: dict) -> User:
#     user = model_update()