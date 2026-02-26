from django.contrib.auth.models import User
from django.db import models


class Batch(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="teacher_profile", null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    subject = models.CharField(max_length=100)
    batch = models.ForeignKey("teachers.Batch", on_delete=models.SET_NULL, null=True, blank=True, related_name="teachers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
