from django.urls import path
from . import views
from .views import TaskCreateView, TaskUpdateView, TaskDeleteView

app_name = "tasks"

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("add/", TaskCreateView.as_view(), name="task_add"),
    path("<int:pk>/edit/", TaskUpdateView.as_view(), name="task_edit"),
    path("<int:pk>/delete/", TaskDeleteView.as_view(), name="task_delete"),
]