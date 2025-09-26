from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django_filters.views import FilterView
from django.urls import reverse_lazy, reverse

from tasks.filters import MaintenanceTaskFilter
from tasks.models import MaintenanceTask, GardenBedTask, MaterialUsage, TaskTool
from tasks.forms import (
    MaintenanceTaskForm,
    GardenBedTaskForm,
    MaterialUsageForm,
    TaskToolForm,
)
from tasks.mixins import TaskObjectPermissionMixin, RelatedTaskPermissionMixin


class TaskListView(LoginRequiredMixin, FilterView):
    model = MaintenanceTask
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"
    filterset_class = MaintenanceTaskFilter
    paginate_by = 10

    login_url = reverse_lazy("login")
    redirect_field_name = "next"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            qs = qs.filter(assigned_to=user)
        return qs


class TaskDetailView(TaskObjectPermissionMixin, DetailView):
    model = MaintenanceTask
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        context["beds"] = task.bed_tasks.select_related("bed")
        context["materials"] = task.materials_used.select_related("material")
        context["tools"] = task.tools_used.select_related("tool")

        context["add_bed_url"] = (
            reverse("tasks:gardenbedtask_create", kwargs={"task_id": task.id})
        )
        context["add_material_url"] = (
            reverse("tasks:materialusage_create", kwargs={"task_id": task.id})
        )
        context["add_tool_url"] = (
            reverse("tasks:tasktool_create", kwargs={"task_id": task.id})
        )
        return context


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = MaintenanceTask
    form_class = MaintenanceTaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    login_url = reverse_lazy("login")
    redirect_field_name = "next"


class TaskUpdateView(LoginRequiredMixin, TaskObjectPermissionMixin, UpdateView):
    model = MaintenanceTask
    form_class = MaintenanceTaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("tasks:task_list")

    login_url = reverse_lazy("login")
    redirect_field_name = "next"


class TaskDeleteView(LoginRequiredMixin, TaskObjectPermissionMixin, DeleteView):
    model = MaintenanceTask
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")

    login_url = reverse_lazy("login")
    redirect_field_name = "next"


class GardenBedTaskCreateView(RelatedTaskPermissionMixin, CreateView):
    model = GardenBedTask
    form_class = GardenBedTaskForm
    template_name = "tasks/gardenbedtask_form.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = task_id
        return initial

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class GardenBedTaskUpdateView(RelatedTaskPermissionMixin, UpdateView):
    model = GardenBedTask
    form_class = GardenBedTaskForm
    template_name = "tasks/gardenbedtask_form.html"

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class GardenBedTaskDeleteView(RelatedTaskPermissionMixin, DeleteView):
    model = GardenBedTask
    template_name = "tasks/gardenbedtask_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class MaterialUsageCreateView(RelatedTaskPermissionMixin, CreateView):
    model = MaterialUsage
    form_class = MaterialUsageForm
    template_name = "tasks/materialusage_form.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = task_id
        return initial

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class MaterialUsageUpdateView(RelatedTaskPermissionMixin, UpdateView):
    model = MaterialUsage
    form_class = MaterialUsageForm
    template_name = "tasks/materialusage_form.html"

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class MaterialUsageDeleteView(RelatedTaskPermissionMixin, DeleteView):
    model = MaterialUsage
    template_name = "tasks/materialusage_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class TaskToolCreateView(RelatedTaskPermissionMixin, CreateView):
    model = TaskTool
    form_class = TaskToolForm
    template_name = "tasks/tasktool_form.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = task_id
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.request.GET.get("task")
        if hasattr(self.object, "task") and self.object.task:
            context["task"] = self.object.task
        elif task_id:
            context["task"] = MaintenanceTask.objects.filter(pk=task_id).first()
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class TaskToolUpdateView(RelatedTaskPermissionMixin, UpdateView):
    model = TaskTool
    form_class = TaskToolForm
    template_name = "tasks/tasktool_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.object.task
        return context

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})


class TaskToolDeleteView(RelatedTaskPermissionMixin, DeleteView):
    model = TaskTool
    template_name = "tasks/tasktool_confirm_delete.html"

    def get_success_url(self):
        return reverse_lazy("tasks:task_detail", kwargs={"pk": self.object.task.id})
