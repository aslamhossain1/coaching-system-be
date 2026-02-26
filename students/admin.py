from django.contrib import admin

from .models import Guardian, Student


@admin.register(Guardian)
class GuardianAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "created_at")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("created_at",)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "phone", "guardian", "batch", "created_at")
    search_fields = ("full_name", "email", "phone")
    list_filter = ("batch", "created_at")
    autocomplete_fields = ("guardian", "batch")
