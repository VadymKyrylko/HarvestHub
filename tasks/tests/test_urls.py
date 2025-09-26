from django.urls import path
from django.http import HttpResponse
from django.views.generic import DetailView, View
from django.shortcuts import get_object_or_404

from tasks.mixins import TaskObjectPermissionMixin, RelatedTaskPermissionMixin
from tasks.models import MaintenanceTask


class DummyTaskDetailView(TaskObjectPermissionMixin, DetailView):
    model = MaintenanceTask

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse("OK")


class DummyRelatedCreateView(RelatedTaskPermissionMixin, View):
    def dispatch(self, request, *args, **kwargs):
        task_id = request.GET.get("task") or kwargs.get("pk")
        if task_id:
            get_object_or_404(MaintenanceTask, pk=task_id)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("OK")


urlpatterns = [
    path("dummy-task/<int:pk>/", DummyTaskDetailView.as_view(), name="dummy_task"),
    path("dummy-related/", DummyRelatedCreateView.as_view(), name="dummy_related"),
]