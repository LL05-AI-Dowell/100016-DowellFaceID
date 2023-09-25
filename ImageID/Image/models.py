from django.db import models
import uuid
import json

class DetectedFace(models.Model):
    face_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image_path = models.ImageField(upload_to='detected_faces/')
    confidence = models.CharField(max_length=200)
    bounding_box = models.TextField(null=True)
    keypoints = models.TextField(null=True)

    def __str__(self):
        return str(self.face_id)
    
    def to_json(self):
        return json.dumps({
            "face_id": str(self.face_id),
            "image_path": str(self.image_path),
            "confidence": self.confidence,
            "bounding_box": json.loads(self.bounding_box) if self.bounding_box else None,
            "keypoints": json.loads(self.keypoints) if self.keypoints else None,
        })
