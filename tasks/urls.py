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
    TaskToolDeleteView
)

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("<int:pk>/", TaskDetailView.as_view(), name="task_detail"),
    path("add/", TaskCreateView.as_view(), name="task_add"),
    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),

    # GardenBedTask
    path("bedtasks/add/", GardenBedTaskCreateView.as_view(), name="gardenbedtask_add"),
    path("bedtasks/<int:pk>/edit/", GardenBedTaskUpdateView.as_view(), name="gardenbedtask_edit"),
    path("bedtasks/<int:pk>/delete/", GardenBedTaskDeleteView.as_view(), name="gardenbedtask_delete"),

    # MaterialUsage
    path("materialusages/add/", MaterialUsageCreateView.as_view(), name="materialusage_add"),
    path("materialusages/<int:pk>/edit/", MaterialUsageUpdateView.as_view(), name="materialusage_edit"),
    path("materialusages/<int:pk>/delete/", MaterialUsageDeleteView.as_view(), name="materialusage_delete"),

    # TaskTool
    path("tasktools/add/", TaskToolCreateView.as_view(), name="tasktool_add"),
    path("tasktools/<int:pk>/edit/", TaskToolUpdateView.as_view(), name="tasktool_edit"),
    path("tasktools/<int:pk>/delete/", TaskToolDeleteView.as_view(), name="tasktool_delete"),
]