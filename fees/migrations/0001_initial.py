from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("students", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Fee",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("due_date", models.DateField()),
                ("paid_date", models.DateField(blank=True, null=True)),
                ("is_paid", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("student", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="fees", to="students.student")),
            ],
        ),
    ]
