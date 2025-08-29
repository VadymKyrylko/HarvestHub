from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from .models import Material
from .forms import MaterialForm


class MaterialListView(ListView):
    model = Material
    template_name = "materials/material_list.html"
    context_object_name = "materials"


class MaterialDetailView(DetailView):
    model = Material
    template_name = "materials/material_detail.html"
    context_object_name = "material"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        material = self.object
        context["tasks"] = material.usages.select_related("task")
        return context


class MaterialCreateView(CreateView):
    model = Material
    form_class = MaterialForm
    template_name = "materials/material_form.html"
    success_url = reverse_lazy("materials:material_list")


class MaterialUpdateView(UpdateView):
    model = Material
    form_class = MaterialForm
    template_name = "materials/material_form.html"
    success_url = reverse_lazy("materials:material_list")


class MaterialDeleteView(DeleteView):
    model = Material
    template_name = "materials/material_confirm_delete.html"
    success_url = reverse_lazy("materials:material_list")
