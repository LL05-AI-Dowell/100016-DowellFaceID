from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    face_encoding = models.BinaryField(null=True, blank=True)