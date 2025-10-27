from django.contrib import admin
from .models import MaintenanceTask, GardenBedTask, MaterialUsage, TaskTool


@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "scheduled_at", "assigned_to")
    list_filter = ("status", "scheduled_at", "assigned_to")
    search_fields = ("name", "description")
    date_hierarchy = "scheduled_at"


@admin.register(GardenBedTask)
class GardenBedTaskAdmin(admin.ModelAdmin):
    list_display = ("task", "bed")
    list_filter = ("bed", "task")
    search_fields = ("task__name", "bed__name")


@admin.register(MaterialUsage)
class MaterialUsageAdmin(admin.ModelAdmin):
    list_display = ("task", "material", "quantity_used")
    list_filter = ("material", "task")
    search_fields = ("task__name", "material__name")


@admin.register(TaskTool)
class TaskToolAdmin(admin.ModelAdmin):
    list_display = ("task", "tool")
    list_filter = ("tool", "task")
    search_fields = ("task__name", "tool__name")
