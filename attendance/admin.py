from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "teacher", "date", "status")
    search_fields = ("student__full_name", "teacher__full_name", "remarks")
    list_filter = ("status", "date", "teacher")
    autocomplete_fields = ("student", "teacher")
    date_hierarchy = "date"
