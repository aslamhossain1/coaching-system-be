from django.contrib import admin

from .models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ("student", "amount", "due_date", "paid_date", "is_paid", "created_at")
    search_fields = ("student__full_name", "student__email")
    list_filter = ("is_paid", "due_date", "paid_date", "created_at")
    autocomplete_fields = ("student",)
    date_hierarchy = "due_date"
