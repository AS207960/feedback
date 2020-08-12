from django.urls import path, include
from . import views

urlpatterns = [
    path('feedback/<uuid:feedback_id>/', views.feedback, name='feedback'),
    path('api/', include('feedback.api.urls')),
]