from django.contrib import admin

from .models import Batch, Teacher


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "start_date", "end_date", "created_at")
    search_fields = ("name", "code")
    list_filter = ("start_date", "end_date", "created_at")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "subject", "batch", "created_at")
    search_fields = ("full_name", "email", "subject")
    list_filter = ("subject", "batch", "created_at")
    autocomplete_fields = ("batch",)
