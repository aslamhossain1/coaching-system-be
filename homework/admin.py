from django.contrib import admin

from .models import Homework


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ("title", "due_date", "teacher", "created_at")
    search_fields = ("title", "description", "teacher__full_name")
    list_filter = ("due_date", "teacher", "created_at")
    autocomplete_fields = ("teacher",)
    date_hierarchy = "due_date"
