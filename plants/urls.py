from django.urls import path
from . import views

urlpatterns = [
    # GardenBed
    path("beds/", views.GardenBedListView.as_view(), name="bed_list"),
    path("beds/<int:pk>/", views.GardenBedDetailView.as_view(), name="bed_detail"),
    path("beds/create/", views.GardenBedCreateView.as_view(), name="bed_create"),
    path("beds/<int:pk>/update/", views.GardenBedUpdateView.as_view(), name="bed_update"),
    path("beds/<int:pk>/delete/", views.GardenBedDeleteView.as_view(), name="bed_delete"),

    # Plant
    path("plants/", views.PlantListView.as_view(), name="plant_list"),
    path("plants/<int:pk>/", views.PlantDetailView.as_view(), name="plant_detail"),
    path("plants/create/", views.PlantCreateView.as_view(), name="plant_create"),
    path("plants/<int:pk>/update/", views.PlantUpdateView.as_view(), name="plant_update"),
    path("plants/<int:pk>/delete/", views.PlantDeleteView.as_view(), name="plant_delete"),

    # BedSection
    path("sections/", views.BedSectionListView.as_view(), name="section_list"),
    path("sections/<int:pk>/", views.BedSectionDetailView.as_view(), name="section_detail"),
    path("sections/create/", views.BedSectionCreateView.as_view(), name="section_create"),
    path("sections/<int:pk>/update/", views.BedSectionUpdateView.as_view(), name="section_update"),
    path("sections/<int:pk>/delete/", views.BedSectionDeleteView.as_view(), name="section_delete"),
]

app_name = "plants"
