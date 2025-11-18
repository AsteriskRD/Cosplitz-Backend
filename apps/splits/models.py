from django.db.models import ForeignKey, IntegerField

from apps.common.models import BaseModel
from apps.users.models import User


from django.db import models

class Splits(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    image_url = models.CharField(null=True, blank=True)
    amount = models.IntegerField(default=0)
    max_participants = models.IntegerField(default=0)
    split_method = models.CharField(max_length=25)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    visibility_radius = models.IntegerField(default=0)
    rules = models.TextField(null=True, blank=True)

# class Split_bubbles(models.Model):
#     split_id = models.ForeignKey(Splits)
#     user_id = models.ForeignKey(User)
#     shared_amount = models.IntegerField(default=0)
#     join_at = models.DateTimeField(null=True, blank=True)