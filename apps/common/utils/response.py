from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status

class APIResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        return Response({
            "success": True,
            "message": message,
            "data": data
        }, status=status_code)

    @staticmethod
    def error(error="An error occurred", details=None, status_code=status.HTTP_400_BAD_REQUEST):
        return Response({
            "success": False,
            "error": error,
            "details": details
        }, status=status_code)

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context['response']

        if response.status_code >= 400:
            custom_response = {
                'status': 'error',
                'message': data.get('detail', 'An error occurred'),
                'errors': data
            }
        else:
            custom_response = {
                'status': 'success',
                'data': data
            }

        return super().render(custom_response, accepted_media_type, renderer_context)
