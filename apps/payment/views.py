from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.common.utils.response import APIResponse
from apps.payment.serializer import CreateVirtualAccountSerializer
from apps.payment.services.flutterwave_service import FlutterwaveService
from apps.payment.services.payment_service import create_virtual_account


class CreateCustomeView(APIView):
    """ API endpoint to create a virtual account for the authenticated user """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        serializer = CreateVirtualAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            response_result = create_virtual_account(user, serializer.validated_data['amount'], serializer.validated_data['narration'])
            return APIResponse().success(data=response_result)
        except Exception as e:
            return APIResponse().error(details=e)

