from django.core.exceptions import PermissionDenied
from .models import MaintenanceTask


class TaskObjectPermissionMixin:
    def has_permission(self, obj):
        user = self.request.user
        return (
            user.is_staff
            or user.is_superuser
            or obj.assigned_to == user
        )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if not self.has_permission(obj):
            raise PermissionDenied("You do not have permission to view this task.")
        return obj


class RelatedTaskPermissionMixin:
    def has_task_permission(self, task):
        user = self.request.user
        return (
            user.is_staff
            or user.is_superuser
            or task.assigned_to == user
        )

    def dispatch(self, request, *args, **kwargs):
        # For CreateView: check task from GET or kwargs
        task_id = request.GET.get("task") or kwargs.get("pk")
        if task_id and not hasattr(self, "object"):
            try:
                task = MaintenanceTask.objects.get(pk=task_id)
            except MaintenanceTask.DoesNotExist:
                raise PermissionDenied("Task not found.")
            if not self.has_task_permission(task):
                raise PermissionDenied("You do not have permission to modify this task.")
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        task = getattr(obj, "task", None)
        if task and not self.has_task_permission(task):
            raise PermissionDenied("You do not have permission to modify this task.")
        return obj
