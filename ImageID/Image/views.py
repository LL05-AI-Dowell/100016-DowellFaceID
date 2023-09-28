# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FaceRecognitionSerializer
import cv2
import face_recognition as fr
from .models import User
import numpy as np
import tempfile
import os
import time

class FaceRecognitionLogin(APIView):
    def post(self, request, format=None):
        serializer = FaceRecognitionSerializer(data=request.data)
        if serializer.is_valid():
            # Initialize the webcam
            video_capture = cv2.VideoCapture(0)

            # Set the duration for capturing frames (e.g., 120 seconds)
            capture_duration = 120  # in seconds
            start_time = time.time()

            captured_face_encoding = None

            while time.time() - start_time < capture_duration:
                # Capture a frame from the webcam
                ret, frame = video_capture.read()

                # Display the frame (optional)
                cv2.imshow('Webcam', frame)

                # Save the captured image temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_image:
                    cv2.imwrite(temp_image.name, frame)

                # Load and encode the captured image
                captured_image = fr.load_image_file(temp_image.name)
                captured_face_encoding = fr.face_encodings(captured_image)

                # If a face is found, break the loop
                if captured_face_encoding:
                    break

                # Delete the temporary image file
                os.remove(temp_image.name)

                # Allow for graceful exit (press 'q' key to stop)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the webcam and destroy the OpenCV window
            video_capture.release()
            cv2.destroyAllWindows()

            if captured_face_encoding:
                captured_face_encoding = captured_face_encoding[0]

                # Compare the captured face encoding with known users
                users = User.objects.all()
                for user in users:
                    if user.face_encoding and fr.compare_faces([user.face_encoding], captured_face_encoding)[0]:
                        return Response({"message": "User authenticated successfully"})

            return Response({"message": "Authentication failed"}, status=403)

        return Response(serializer.errors, status=400)
