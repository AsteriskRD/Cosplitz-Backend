from  .models import User
from ..common.utils import get_object


def user_get(user_id):
    # user = User.objects.get(id=user_id)
    user = get_object(User, id=user_id)
    return user