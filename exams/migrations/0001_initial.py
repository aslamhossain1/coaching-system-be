from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("teachers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Exam",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("exam_date", models.DateField()),
                ("total_marks", models.PositiveIntegerField(default=100)),
                ("teacher", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="teachers.teacher")),
            ],
        ),
    ]
