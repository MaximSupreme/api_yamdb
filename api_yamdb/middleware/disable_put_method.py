from django.http import JsonResponse
from rest_framework import status

class DisablePutMethodMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'PUT' and any(
                path in request.path for path in [
                    '/comments/', '/reviews/', '/titles/']):
            return JsonResponse(
                {'detail': 'PUT method is not allowed on this resource.'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )
        response = self.get_response(request)
        return response
