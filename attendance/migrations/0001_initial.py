from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("students", "0001_initial"),
        ("teachers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Attendance",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("date", models.DateField()),
                ("status", models.CharField(choices=[("present", "Present"), ("absent", "Absent"), ("late", "Late")], default="present", max_length=10)),
                ("remarks", models.TextField(blank=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="attendance_records", to="students.student")),
                ("teacher", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="teachers.teacher")),
            ],
            options={"unique_together": {("student", "date")}},
        ),
    ]
