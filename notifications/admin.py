from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "student", "teacher", "is_read", "created_at")
    search_fields = ("title", "message", "student__full_name", "teacher__full_name")
    list_filter = ("is_read", "teacher", "created_at")
    autocomplete_fields = ("student", "teacher")
