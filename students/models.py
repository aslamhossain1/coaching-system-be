from django.contrib.auth.models import User
from django.db import models


class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="guardian_profile", null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile", null=True, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    guardian = models.ForeignKey("students.Guardian", on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    batch = models.ForeignKey("teachers.Batch", on_delete=models.SET_NULL, null=True, blank=True, related_name="students")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name
