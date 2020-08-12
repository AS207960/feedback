from rest_framework import serializers
from .. import models


class FeedbackRequestSerializer(serializers.ModelSerializer):
    public_url = serializers.URLField(read_only=True)
    creator = serializers.CharField(read_only=True)

    class Meta:
        model = models.FeedbackRequest
        fields = ('url', 'id', 'creator', 'action_reference', 'description', 'rating', 'liked', 'disliked',
                  'other_comments', 'public_url')
