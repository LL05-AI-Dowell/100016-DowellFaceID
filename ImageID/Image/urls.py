from django.urls import path
from .views import FaceRecognitionLogin

urlpatterns = [
    path('login/', FaceRecognitionLogin.as_view(), name='login'),
]