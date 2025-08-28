from django.contrib import admin
from .models import GardenBed, Plant, BedSection


@admin.register(GardenBed)
class GardenBedAdmin(admin.ModelAdmin):
    list_display = ("name", "length", "width", "area")
    search_fields = ("name",)

    @admin.display(description="Area (m²)")
    def area(self, obj):
        return obj.area


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("name", "space_per_plant", "max_plants_per_m2")
    search_fields = ("name",)

    @admin.display(description="Max plants per 1 m²")
    def max_plants_per_m2(self, obj):
        if obj.space_per_plant > 0:
            return round(1 / obj.space_per_plant, 2)
        return "—"


@admin.register(BedSection)
class BedSectionAdmin(admin.ModelAdmin):
    list_display = (
        "bed",
        "plant",
        "plant_count",
        "required_area",
        "max_possible_plants"
    )
    list_filter = ("bed", "plant")

    @admin.display(description="Required area (m²)")
    def required_area(self, obj):
        return obj.required_area

    @admin.display(description="Max possible plants")
    def max_possible_plants(self, obj):
        if obj.plant.space_per_plant > 0:
            return int(obj.bed.area // obj.plant.space_per_plant)
        return "—"
