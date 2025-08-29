from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django_filters.views import FilterView
from django.http import Http404
from django.urls import reverse_lazy

from tasks.filters import MaintenanceTaskFilter
from tasks.models import (
    MaintenanceTask,
    GardenBedTask,
    MaterialUsage,
    TaskTool)
from tasks.forms import (
    MaintenanceTaskForm,
    GardenBedTaskForm,
    MaterialUsageForm,
    TaskToolForm
)


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


class TaskDetailView(DetailView):
    model = MaintenanceTask
    template_name = "tasks/task_detail.html"
    context_object_name = "task"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            if obj.assigned_to != user:
                raise Http404("You do not have permission to view this task.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object
        context["beds"] = task.bed_tasks.select_related("bed")
        context["materials"] = task.materials_used.select_related("material")
        context["tools"] = task.tools_used.select_related("tool")

        context["add_bed_url"] = reverse_lazy(
            "tasks:gardenbedtask_add"
        ) + f"?task={task.id}"
        context["add_material_url"] = reverse_lazy(
            "tasks:materialusage_add"
        ) + f"?task={task.id}"
        context["add_tool_url"] = reverse_lazy(
            "tasks:tasktool_add"
        ) + f"?task={task.id}"
        return context


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            if obj.assigned_to != user:
                raise Http404("You do not have permission to edit this task.")
        return obj


class TaskDeleteView(DeleteView):
    model = MaintenanceTask
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("tasks:task_list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user
        if not user.is_staff and not user.is_superuser:
            if obj.assigned_to != user:
                raise Http404(
                    "You do not have permission to delete this task."
                )
        return obj


class GardenBedTaskCreateView(CreateView):
    model = GardenBedTask
    form_class = GardenBedTaskForm
    template_name = "tasks/gardenbedtask_form.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = task_id
        return initial

    def dispatch(self, request, *args, **kwargs):
        task_id = request.GET.get("task") or self.kwargs.get("pk")
        if task_id:
            task = MaintenanceTask.objects.get(pk=task_id)
            if not request.user.is_staff and not request.user.is_superuser:
                if task.assigned_to != request.user:
                    raise Http404(
                        "You do not have permission to modify this task."
                    )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class GardenBedTaskUpdateView(UpdateView):
    model = GardenBedTask
    form_class = GardenBedTaskForm
    template_name = "tasks/gardenbedtask_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (not self.request.user.is_staff
                and not self.request.user.is_superuser):
            if obj.task.assigned_to != self.request.user:
                raise Http404("You do not have permission to edit this.")
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class GardenBedTaskDeleteView(DeleteView):
    model = GardenBedTask
    template_name = "tasks/gardenbedtask_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (not self.request.user.is_staff
                and not self.request.user.is_superuser):
            if obj.task.assigned_to != self.request.user:
                raise Http404("You do not have permission to delete this.")
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class MaterialUsageCreateView(CreateView):
    model = MaterialUsage
    form_class = MaterialUsageForm
    template_name = "tasks/materialusage_form.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = task_id
        return initial

    def dispatch(self, request, *args, **kwargs):
        task_id = request.GET.get("task") or self.kwargs.get("pk")
        if task_id:
            task = MaintenanceTask.objects.get(pk=task_id)
            if not request.user.is_staff and not request.user.is_superuser:
                if task.assigned_to != request.user:
                    raise Http404(
                        "You do not have permission to modify this task."
                    )
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class MaterialUsageUpdateView(UpdateView):
    model = MaterialUsage
    form_class = MaterialUsageForm
    template_name = "tasks/materialusage_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (not self.request.user.is_staff
                and not self.request.user.is_superuser):
            if obj.task.assigned_to != self.request.user:
                raise Http404("You do not have permission to edit this.")
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class MaterialUsageDeleteView(DeleteView):
    model = MaterialUsage
    template_name = "tasks/materialusage_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (not self.request.user.is_staff
                and not self.request.user.is_superuser):
            if obj.task.assigned_to != self.request.user:
                raise Http404("You do not have permission to delete this.")
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class TaskToolCreateView(CreateView):
    model = TaskTool
    form_class = TaskToolForm
    template_name = "tasks/tasktool_form.html"

    def get_initial(self):
        initial = super().get_initial()
        task_id = self.request.GET.get("task")
        if task_id:
            initial["task"] = task_id
        return initial

    def dispatch(self, request, *args, **kwargs):
        task_id = self.request.GET.get("task") or self.kwargs.get("pk")
        if task_id:
            task = MaintenanceTask.objects.get(pk=task_id)
            if not request.user.is_staff and not request.user.is_superuser:
                if task.assigned_to != request.user:
                    raise Http404(
                        "You do not have permission to modify this task."
                    )
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.request.GET.get("task")
        if hasattr(self.object, "task") and self.object.task:
            context["task"] = self.object.task
        elif task_id:
            context["task"] = MaintenanceTask.objects.filter(
                pk=task_id
            ).first()
        return context

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class TaskToolUpdateView(UpdateView):
    model = TaskTool
    form_class = TaskToolForm
    template_name = "tasks/tasktool_form.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (not self.request.user.is_staff
                and not self.request.user.is_superuser):
            if obj.task.assigned_to != self.request.user:
                raise Http404("You do not have permission to edit this.")
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task"] = self.object.task
        return context

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )


class TaskToolDeleteView(DeleteView):
    model = TaskTool
    template_name = "tasks/tasktool_confirm_delete.html"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if (not self.request.user.is_staff
                and not self.request.user.is_superuser):
            if obj.task.assigned_to != self.request.user:
                raise Http404(
                    "You do not have permission to delete this."
                )
        return obj

    def get_success_url(self):
        return reverse_lazy(
            "tasks:task_detail",
            kwargs={"pk": self.object.task.id}
        )
