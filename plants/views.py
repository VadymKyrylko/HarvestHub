from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import GardenBed, Plant, BedSection

class BaseListView(ListView):
    context_object_name = "objects"


class BaseDetailView(DetailView):
    context_object_name = "object"


class BaseCreateView(CreateView):
    success_url = None


class BaseUpdateView(UpdateView):
    success_url = None


class BaseDeleteView(DeleteView):
    success_url = None

class GardenBedListView(BaseListView):
    model = GardenBed
    context_object_name = "garden_beds"
    template_name = "plants/gardenbed/bed_list.html"

class GardenBedDetailView(BaseDetailView):
    model = GardenBed
    template_name = "plants/gardenbed/bed_detail.html"

class GardenBedCreateView(BaseCreateView):
    model = GardenBed
    fields = ["name", "length", "width"]
    template_name = "plants/gardenbed/bed_form.html"
    success_url = reverse_lazy("plants:bed_list")

class GardenBedUpdateView(BaseUpdateView):
    model = GardenBed
    fields = ["name", "length", "width"]
    template_name = "plants/gardenbed/bed_form.html"
    success_url = reverse_lazy("plants:bed_list")

class GardenBedDeleteView(BaseDeleteView):
    model = GardenBed
    template_name = "plants/gardenbed/bed_confirm_delete.html"
    success_url = reverse_lazy("plants:bed_list")

class PlantListView(BaseListView):
    model = Plant
    context_object_name = "plants"
    template_name = "plants/plant/plant_list.html"

class PlantDetailView(BaseDetailView):
    model = Plant
    template_name = "plants/plant/plant_detail.html"

class PlantCreateView(BaseCreateView):
    model = Plant
    fields = ["name", "type", "spacing"]
    template_name = "plants/plant/plant_form.html"
    success_url = reverse_lazy("plants:plant_list")

class PlantUpdateView(BaseUpdateView):
    model = Plant
    fields = ["name", "type", "spacing"]
    template_name = "plants/plant/plant_form.html"
    success_url = reverse_lazy("plants:plant_list")

class PlantDeleteView(BaseDeleteView):
    model = Plant
    template_name = "plants/plant/plant_confirm_delete.html"
    success_url = reverse_lazy("plants:plant_list")

class BedSectionListView(BaseListView):
    model = BedSection
    context_object_name = "sections"
    template_name = "plants/section/section_list.html"

class BedSectionDetailView(BaseDetailView):
    model = BedSection
    template_name = "plants/section/section_detail.html"

class BedSectionCreateView(BaseCreateView):
    model = BedSection
    fields = ["garden_bed", "name", "area"]
    template_name = "plants/section/section_form.html"
    success_url = reverse_lazy("plants:section_list")

class BedSectionUpdateView(BaseUpdateView):
    model = BedSection
    fields = ["garden_bed", "name", "area"]
    template_name = "plants/section/section_form.html"
    success_url = reverse_lazy("plants:section_list")

class BedSectionDeleteView(BaseDeleteView):
    model = BedSection
    template_name = "plants/section/section_confirm_delete.html"
    success_url = reverse_lazy("plants:section_list")