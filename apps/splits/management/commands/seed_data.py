import datetime

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from decimal import Decimal
import random

from apps.splits.models import Splits, SplitParticipants

User = get_user_model()


class Command(BaseCommand):
    help = "Seed dummy users, splits, and split participants"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding data...")

        # -------------------
        # Create Users
        # -------------------
        users = []
        for i in range(1, 6):
            user, _ = User.objects.get_or_create(
                email=f"user{i}@test.com",
                defaults={
                    "username": f"user{i}",
                    "password": "password123"
                }
            )
            users.append(user)

        # -------------------
        # Create Splits
        # -------------------
        splits = []
        for i in range(1, 4):
            split = Splits.objects.create(
                user_id=i,
                title=f"Split {i}",
                category="Dummy split data",
                amount=Decimal("3000.00"),
                max_participants=3,
                status="active",
                image_url="https/124422_images",
                start_date=datetime.date.today(),
                end_date=datetime.date.today(),
                location="Ogun state",

            )
            splits.append(split)

        # -------------------
        # Create Participants
        # -------------------
        for split in splits:
            participants = random.sample(users, 2)

            for user in participants:
                SplitParticipants.objects.get_or_create(
                    split=split,
                    user=user,
                    shared_amount= 1000,
                )

        self.stdout.write(self.style.SUCCESS("Dummy data seeded successfully ✅"))
