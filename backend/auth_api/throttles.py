from rest_framework.exceptions import Throttled


def check_throttle_duration(self, request):
    """
    Check duration for throttling
    """
    throttle_durations = []
    for throttle in self.get_throttles():
        if not throttle.allow_request(request, self):
            throttle_durations.append(throttle.wait())

    return throttle_durations


def start_throttle(throttle_durations, request):
    """
    Custom throttle function to replace self.throttled.
    Raises a Throttled exception with a custom detail message based on the request URL.
    """
    durations = [duration for duration in throttle_durations if duration is not None]

    wait = max(durations, default=None)

    # Map URL names to custom throttle messages
    throttle_messages = {
        "login": "Too many login attempts.",
        "resend-otp": "Too many OTP resend requests.",
        "email-verify": "Too many email verification requests.",
        "phone-verify": "Too many phone verification requests.",
        "password-reset": "Too many password reset requests.",
        "user-list": "Too many user creation requests.",
    }

    # Get the URL name from the request
    url_name = request.resolver_match.url_name if request.resolver_match else None
    # Default message if URL name is not found
    default_message = "Request limit exceeded. Please try again later."

    # Get the custom message based on URL name
    detail = throttle_messages.get(url_name, default_message)

    raise Throttled(detail=detail, wait=wait)
