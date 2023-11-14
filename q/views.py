
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import face_recognition


import uuid

import os
from django.conf import settings
import numpy as np

import PIL.Image


class FaceDetection(APIView):
    def post(self, request, *args, **kwargs):
        img = request.data.get('image')

        if img:
            try:
                # Load the image and convert it to a format that face_recognition understands
                image = PIL.Image.open(img)
                image_array = np.array(image)

                # Detect faces in the image
                face_locations = face_recognition.face_locations(image_array)

                # Create a list to store information about detected faces
                detected_faces = []

                # Loop through detected face locations and extract information
                for face_location in face_locations:
                    top, right, bottom, left = face_location

                    # Add face location information to the list
                    detected_faces.append({
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                        "left": left
                    })

                return Response({"detected_faces": detected_faces}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "No image provided"}, status=status.HTTP_400_BAD_REQUEST)


class Image(APIView):
    def post(self, request, *args, **kwargs):
        img = request.data.get('image')  # Use the correct field name
        if img:
            img_extension = os.path.splitext(img.name)[-1]
            file_path = os.path.join(
                settings.MEDIA_ROOT, str(uuid.uuid4()) + img_extension)
            with open(file_path, 'wb') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            return Response({"success": "accepted"}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)
