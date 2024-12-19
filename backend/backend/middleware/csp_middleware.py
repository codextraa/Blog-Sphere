from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class CustomCSPMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Default CSP: More restrictive
        csp_header = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self'; font-src 'self'; object-src 'none';"

        # If the request is for Swagger UI, apply a more lenient CSP
        if request.path.startswith('/api/docs/'):
            csp_header = (
                "default-src 'self'; "
                "img-src 'self' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
                "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://apis.google.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "connect-src 'self'; "
                "frame-src 'self'; "
                "object-src 'none'; "
                "child-src 'none';"
            )

        # Add the CSP header to the response
        response['Content-Security-Policy'] = csp_header
        return response
