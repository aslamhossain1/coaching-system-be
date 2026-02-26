from django.db import models


class Notification(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True, related_name="notifications")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
