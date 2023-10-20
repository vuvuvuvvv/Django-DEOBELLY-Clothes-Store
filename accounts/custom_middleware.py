# custom_middleware.py
from django.shortcuts import redirect
from django.urls import reverse, resolve


class ValidatedCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if self.should_check_validate(request):
            if request.user.is_authenticated:
                if request.user.is_verified == 0 and request.user.is_superuser == 0:
                    return redirect("validate_infor_user")
                else:
                    response = self.get_response(request)
                    return response
            else:
                return redirect("login")
        else:
            response = self.get_response(request)
            return response

    def should_check_validate(self, request):
        # Define a list of URL patterns that should trigger the validate check.
        protected_url_patterns = [
            # "reset", 
            "cart",
            "checkout"
        ]
        # Use Django's URL resolver to match the request's path to URL patterns.
        match = resolve(request.path)
        # Check if the resolved URL pattern name is in the list of protected patterns.
        if match.route.split("/")[0] in protected_url_patterns:
            return True
        else:
            return False
