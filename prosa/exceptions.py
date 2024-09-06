from django.http import JsonResponse
from django.urls import resolve, Resolver404

class HandleInvalidUrlMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolve(request.path)
        except Resolver404:
            return JsonResponse({"detail": "Essa rota não existe."}, status=404)
        response = self.get_response(request)
        return response