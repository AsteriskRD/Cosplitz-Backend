from apps.payment.models import UserAccountDetails
from apps.payment.services.flutterwave_service import FlutterwaveService
from apps.users.models import User
import uuid


def get_or_create_customer(user: User):
    customer_details = UserAccountDetails.objects.filter(user=user).first()
    if customer_details:
        return customer_details

    service = FlutterwaveService()
    result = service.create_customer(
        user.first_name,
        user.last_name,
        user.email,
    )
    if result.get('status') == 'success':
        customer_id = str(result.get('data').get('customer_id'))
        details = UserAccountDetails.objects.create(user=user, customer_id=customer_id)
        return details
    return None

def create_virtual_account(user: User, amount:str , narration :str) :
    user_account_details = get_or_create_customer(user)
    if not user_account_details:
        return {"error": "Could not create or find customer details"}

    idempotency_key =  f"{user.id}_pay_{uuid.uuid4()}"
    reference = str(uuid.uuid4())
    payload = {
        "reference": reference,
        "customer_id": user_account_details.customer_id,
        "expiry": 1,
        "amount": amount,
        "currency": user_account_details.currency,
        "account_type": user_account_details.account_type,
        "narration": narration
    }

    flutterwave_service = FlutterwaveService(idempotency_key)
    result = flutterwave_service.create_virtual_account(payload=payload)

    if result.get('status') == 'success':
        user_account_details.reference = reference
        user_account_details.idempotency_key = idempotency_key
        user_account_details.save()
    return  result
