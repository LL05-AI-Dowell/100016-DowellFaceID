# serializers.py
from rest_framework import serializers

class FaceRecognitionSerializer(serializers.Serializer):
    image = serializers.ImageField()


