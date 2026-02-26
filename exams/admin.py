from django.contrib import admin

from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "exam_date", "total_marks", "teacher")
    search_fields = ("title", "teacher__full_name")
    list_filter = ("exam_date", "teacher")
    autocomplete_fields = ("teacher",)
    date_hierarchy = "exam_date"
