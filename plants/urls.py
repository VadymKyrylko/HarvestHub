from django.urls import path
from . import views
from plants.views import (
    GardenBedListView,
GardenBedDetailView,
GardenBedCreateView,
GardenBedUpdateView,
GardenBedDeleteView,
PlantListView,
PlantDetailView,
PlantCreateView,
PlantUpdateView,
PlantDeleteView,
BedSectionListView,
BedSectionDetailView,
BedSectionCreateView,
BedSectionUpdateView,
BedSectionDeleteView,
)

urlpatterns = [
    # GardenBed
    path("beds/", GardenBedListView.as_view(), name="bed_list"),
    path("beds/<int:pk>/", GardenBedDetailView.as_view(), name="bed_detail"),
    path("beds/create/", GardenBedCreateView.as_view(), name="bed_create"),
    path("beds/<int:pk>/update/", GardenBedUpdateView.as_view(), name="bed_update"),
    path("beds/<int:pk>/delete/", GardenBedDeleteView.as_view(), name="bed_delete"),

    # Plant
    path("plants/", PlantListView.as_view(), name="plant_list"),
    path("plants/<int:pk>/", PlantDetailView.as_view(), name="plant_detail"),
    path("plants/create/", PlantCreateView.as_view(), name="plant_create"),
    path("plants/<int:pk>/update/", PlantUpdateView.as_view(), name="plant_update"),
    path("plants/<int:pk>/delete/", PlantDeleteView.as_view(), name="plant_delete"),

    # BedSection
    path("sections/", BedSectionListView.as_view(), name="section_list"),
    path("sections/<int:pk>/", BedSectionDetailView.as_view(), name="section_detail"),
    path("sections/create/", BedSectionCreateView.as_view(), name="section_create"),
    path("sections/<int:pk>/update/", BedSectionUpdateView.as_view(), name="section_update"),
    path("sections/<int:pk>/delete/", BedSectionDeleteView.as_view(), name="section_delete"),
]

app_name = "plants"
