from .models import DetectedFace
from rest_framework import serializers

class DetectedFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetectedFace
        fields = ['face_id', 'image_path', 'confidence', 'bounding_box', 'keypoints']

