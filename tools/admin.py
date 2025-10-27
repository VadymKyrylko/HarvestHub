from django.contrib import admin
from .models import Tool


@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "is_checked_out")
    list_filter = ("status", "is_checked_out")
    search_fields = ("name",)
