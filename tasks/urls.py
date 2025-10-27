from django.urls import path
from . import views
from .views import (
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TaskDetailView,
    GardenBedTaskCreateView,
    GardenBedTaskUpdateView,
    GardenBedTaskDeleteView,
    MaterialUsageCreateView,
    MaterialUsageUpdateView,
    MaterialUsageDeleteView,
    TaskToolCreateView,
    TaskToolUpdateView,
    TaskToolDeleteView,
)

app_name = "tasks"

urlpatterns = [
    # Tasks
    path("", views.TaskListView.as_view(), name="task_list"),
    path("new/", TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("<int:pk>/update/", TaskUpdateView.as_view(), name="task_update"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
    # GardenBedTasks
    path(
        "<int:task_id>/beds/new/",
        GardenBedTaskCreateView.as_view(),
        name="gardenbedtask_create",
    ),
    path(
        "<int:task_id>/beds/<int:pk>/update/",
        GardenBedTaskUpdateView.as_view(),
        name="gardenbedtask_update",
    ),
    path(
        "<int:task_id>/beds/<int:pk>/delete/",
        GardenBedTaskDeleteView.as_view(),
        name="gardenbedtask_delete",
    ),
    # MaterialUsage
    path(
        "<int:task_id>/materials/new/",
        MaterialUsageCreateView.as_view(),
        name="materialusage_create",
    ),
    path(
        "<int:task_id>/materials/<int:pk>/update/",
        MaterialUsageUpdateView.as_view(),
        name="materialusage_update",
    ),
    path(
        "<int:task_id>/materials/<int:pk>/delete/",
        MaterialUsageDeleteView.as_view(),
        name="materialusage_delete",
    ),
    # TaskTool
    path(
        "<int:task_id>/tools/new/",
        TaskToolCreateView.as_view(),
        name="tasktool_create"
    ),
    path(
        "<int:task_id>/tools/<int:pk>/update/",
        TaskToolUpdateView.as_view(),
        name="tasktool_update",
    ),
    path(
        "<int:task_id>/tools/<int:pk>/delete/",
        TaskToolDeleteView.as_view(),
        name="tasktool_delete",
    ),
]
