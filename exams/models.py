from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    exam_date = models.DateField()
    total_marks = models.PositiveIntegerField(default=100)
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
