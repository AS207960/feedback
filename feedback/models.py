from django.db import models
from django.shortcuts import reverse
from django.conf import settings
import uuid


class FeedbackRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    creator = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    action_reference = models.CharField(max_length=255, blank=True, null=True)
    rating = models.SmallIntegerField(blank=True, null=True)
    liked = models.TextField(blank=True, null=True)
    disliked = models.TextField(blank=True, null=True)
    other_comments = models.TextField(blank=True, null=True)

    def public_url(self):
        return settings.EXTERNAL_URL_BASE + reverse('feedback', args=(self.id,))
