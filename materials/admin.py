from django.contrib import admin
from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "get_unit_display_value")
    list_filter = ("unit",)
    search_fields = ("name",)

    def get_unit_display_value(self, obj):
        return obj.get_unit_display()
    get_unit_display_value.short_description = "Unit (display)"