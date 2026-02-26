from django.db import models


class Attendance(models.Model):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"

    STATUS_CHOICES = [
        (PRESENT, "Present"),
        (ABSENT, "Absent"),
        (LATE, "Late"),
    ]

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="attendance_records")
    teacher = models.ForeignKey("teachers.Teacher", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PRESENT)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student} - {self.date}"
