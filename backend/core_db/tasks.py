import logging
from celery import shared_task
from django.utils import timezone
from rest_framework_simplejwt.tokens import OutstandingToken

logger = logging.getLogger(__name__)


# Background task to clean up expired refresh tokens
@shared_task
def cleanup_expired_tokens():
    """Clean up expired refresh tokens."""
    expired_tokens = OutstandingToken.objects.filter(expires_at__lt=timezone.now())
    count = expired_tokens.count()
    expired_tokens.delete()
    logger.info("Deleted %s expired refresh tokens", count)
