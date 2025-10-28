from typing import Optional

from django.db import transaction

from .models import User
from apps.common.services import model_update
from typing import List, Optional


@transaction.atomic
def user_create(*, email:str, password:Optional[str] =None, **extra_fields ) -> User:
    user = User.objects.create_user(email=email, password=password, **extra_fields)
    return user

@transaction.atomic
def user_update(*, user: User, data) -> User:
    non_side_effect_fields: List[str] = [
        # "first_name",
        # "last_name"
    ]

    user, has_updated = model_update(instance=user, fields=non_side_effect_fields, data=data)

    # Side-effect fields update here (e.g. username is generated based on first & last name)

    # ... some additional tasks with the user ...

    return user
