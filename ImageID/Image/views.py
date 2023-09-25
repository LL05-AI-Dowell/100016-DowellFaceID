import os
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from mtcnn.mtcnn import MTCNN
from numpy import asarray
from PIL import Image 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DetectedFace
from .serializers import DetectedFaceSerializer

@api_view(['POST', 'GET'])
def image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            try:
                # Upload the image and get its path
                img = request.FILES['image']
                img_extension = os.path.splitext(img.name)[-1]
                image_path = default_storage.save(settings.MEDIA_URL + str(uuid.uuid4()) + img_extension, img)

                # Detect faces in the uploaded image
                detected_faces = detect_faces_in_image(image_path)

                # Serialize the detected faces and save them to the database
                serialized_faces = []
                for face_data in detected_faces:
                    detected_face = DetectedFace.objects.create(
                        image_path=image_path,
                        confidence=face_data["confidence"],
                        bounding_box=face_data["box"],
                        keypoints=face_data["keypoints"]
                    )
                    serialized_face = DetectedFaceSerializer(detected_face).data
                    serialized_faces.append(serialized_face)

                return Response({"detected_faces": serialized_faces}, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"message": "No 'image' file provided in the request."}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        # Handle the GET request to retrieve a list of detected faces
        detected_faces = DetectedFace.objects.all()
        serialized_faces = DetectedFaceSerializer(detected_faces, many=True).data
        return Response({"detected_faces": serialized_faces}, status=status.HTTP_200_OK)

def detect_faces_in_image(image_path):
    image = Image.open(default_storage.open(image_path))
    image = image.convert('RGB')
    pixels = asarray(image)

    detector = MTCNN()

    # Detect faces in the image
    results = detector.detect_faces(pixels)

    # Extract the bounding box from the faces
    detected_faces = []

    for result in results:
        # Only detect faces with a confidence of 90% and above
        if result['confidence'] > 0.90:
            detected_faces.append({
                "confidence": result['confidence'],
                "box": result['box'],
                "keypoints": result['keypoints']
            })

    return detected_faces