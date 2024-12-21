from django.middleware.csrf import CsrfViewMiddleware

class CustomCsrfMiddleware(CsrfViewMiddleware):
    def _set_token(self, request, response):
        # Overriding to avoid setting the CSRF token in cookies
        pass