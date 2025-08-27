from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import MaintenanceTask
from .forms import MaintenanceTaskForm

class TaskListView(ListView):
    model = MaintenanceTask
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

class TaskCreateView(CreateView):
    model = MaintenanceTask
    form_class = MaintenanceTaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

class TaskUpdateView(UpdateView):
    model = MaintenanceTask
    form_class = MaintenanceTaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

class TaskDeleteView(DeleteView):
    model = MaintenanceTask
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")