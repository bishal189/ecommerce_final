# middleware.py

from django.http import HttpResponseNotFound

class SellerAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated and if the user is a seller
        if request.user.is_authenticated and request.user.is_seller:
            # If the user is a seller and the URL doesn't contain '/account/', return 404
            if ('/account/' not in request.path) and ('/media/' not in request.path):
                return HttpResponseNotFound("Page does not exist.")

        response = self.get_response(request)
        return response
