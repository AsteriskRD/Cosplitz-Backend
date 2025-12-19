from django.db import transaction

from apps.splits.models import Splits, SplitParticipants


def get_split_for_join(split_id):
    """
    Fetch and lock split row for safe concurrent joins
    """
    return Splits.objects.select_for_update().get(id=split_id)

def validate_join_split(split, user):
    """ Validate if user can join split """
    """ Check if split is active """
    if split.status != "active" :
        raise Exception("Split already Inactive")

    """ Check if user as joined split """
    if SplitParticipants.objects.filter(user=user, split=split).exists():
        raise Exception("User already joined this split ")

    """ Check for max participants """

def calculate_share_amount(split):
    return split.amount / split.max_participants

def add_participant_split(split, user):
    shared_amount = calculate_share_amount(split)

    SplitParticipants.objects.create(
        split=split,
        user=user,
        shared_amount=shared_amount,
    )

def update_split_status(split):
    split_participants = SplitParticipants.objects.filter(split=split).count()
    if split_participants == split.max_participants:
        split.status = "inactive"
        split.save(update_fields=['status'])

def join_split(split_id, user) :
    with transaction.atomic():
        split = get_split_for_join(split_id)

        validate_join_split(split, user)

        add_participant_split(split, user)

        """update split"""
        update_split_status(split)

        return split



def fetch_splits_joined_by_user(user):
    return (
        Splits.objects
        .filter(splitparticipants__user=user)
        .distinct()
    )
