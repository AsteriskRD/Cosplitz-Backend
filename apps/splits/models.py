from django.db.models import ForeignKey, IntegerField

from apps.common.models import BaseModel
from apps.users.models import User
# from cloundary.model import


from django.db import models

class Splits(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    image_url = models.ImageField(upload_to='splits/',null=True, blank=True)
    amount = models.IntegerField(default=0)
    max_participants = models.IntegerField(default=0)
    split_method = models.CharField(max_length=25)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)
    visibility_radius = models.IntegerField(default=0)
    rules = models.TextField(null=True, blank=True)
    status = models.CharField(default="active", max_length=10)

class SplitParticipants(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    split = models.ForeignKey(
        Splits,
        on_delete=models.CASCADE,
        related_name='splitparticipants')
    shared_amount = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['user', 'split']

    def __str__(self):
        return f"{self.user} joined {self.split}"


# class Split_bubbles(models.Model):
#     split_id = models.ForeignKey(Splits)
#     user_id = models.ForeignKey(User)
#     shared_amount = models.IntegerField(default=0)
#     join_at = models.DateTimeField(null=True, blank=True)