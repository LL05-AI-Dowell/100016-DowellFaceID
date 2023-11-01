# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-one relationship with the built-in User model
    face_features = models.ImageField(null=True, blank=True)
    encoding = models.BinaryField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
