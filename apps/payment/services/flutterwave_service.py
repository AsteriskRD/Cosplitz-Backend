import requests
from typing import Dict, Any

from django.conf import settings


class FlutterwaveService:
    """Service class to handle all Flutterwave API communications"""
    BASE_URL = settings.FLUTTERWAVE_BASE_URL

    def __init__(self, idempotency_key: str = None):
        self.secret_key = settings.FLUTTERWAVE_SECRET_KEY
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.secret_key,
        }
        if idempotency_key:
           self.headers['X-Idempotency-Key'] =idempotency_key

    def create_customer(self,first_name : str, last_name : str, email : str) -> Dict[str, Any] :
        """ Create a new customer """
        url = f"{self.BASE_URL}/customers"

        payload = {
            "name": {
                "first": first_name,
                "last": last_name
            },
            "email": email
        }

        response = requests.post(url, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_virtual_account(self, payload):
        url = f"{self.BASE_URL}/virtual-accounts"
        response = requests.post(url, json=payload, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()