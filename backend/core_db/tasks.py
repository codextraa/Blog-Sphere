import math
import random
import logging
from celery import shared_task
from django.utils import timezone
from django.db import models
from rest_framework_simplejwt.tokens import OutstandingToken
from core_db.models import Blog


logger = logging.getLogger(__name__)


# Background task to update blog scores
@shared_task
def update_blog_scores():
    max_likes = Blog.objects.aggregate(max_likes=models.Max("likes"))["max_likes"] or 1
    now = timezone.now()
    blogs_to_update = []

    for blog in Blog.objects.filter(status="Published", visibility=True):
        likes_score = blog.likes / max_likes if max_likes > 0 else 0
        time_diff = (now - blog.created_at).total_seconds() / 3600
        recency_score = 1 / (1 + math.log1p(max(time_diff, 1)))
        random_factor = random.uniform(0, 0.1)
        score = (0.4 * likes_score) + (0.5 * recency_score) + (0.1 * random_factor)
        blog.score = score
        blogs_to_update.append(blog)

    Blog.objects.bulk_update(blogs_to_update, ["score"])


# Background task to clean up expired refresh tokens
@shared_task
def cleanup_expired_tokens():
    """Clean up expired refresh tokens."""
    expired_tokens = OutstandingToken.objects.filter(expires_at__lt=timezone.now())
    count = expired_tokens.count()
    expired_tokens.delete()
    logger.info("Deleted %s expired refresh tokens", count)
