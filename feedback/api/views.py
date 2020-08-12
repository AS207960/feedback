from rest_framework import viewsets, exceptions
from rest_framework.permissions import DjangoModelPermissions
from django.core.exceptions import PermissionDenied
from . import serializers, auth
from .. import models


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class FeedbackRequestViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FeedbackRequestSerializer
    queryset = models.FeedbackRequest.objects.all()
    permission_classes = [CustomDjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user.username)
