from django.urls import include, path
from rest_framework import routers, schemas
from . import views

router = routers.DefaultRouter()
router.register(r'feedback_request', views.FeedbackRequestViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('openapi', schemas.get_schema_view(
        title="Glauca Feedback",
        version="0.0.1"
    ), name='openapi-schema'),
]