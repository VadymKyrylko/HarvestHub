from django.urls import path
from . import views
from .views import (
    ToolCreateView,
    ToolUpdateView,
    ToolDeleteView,
    ToolDetailView
)

app_name = "tools"

urlpatterns = [
    path("", views.ToolListView.as_view(), name="tool_list"),
    path("<int:pk>/", ToolDetailView.as_view(), name="tool_detail"),
    path("add/", ToolCreateView.as_view(), name="tool_add"),
    path("<int:pk>/edit/", ToolUpdateView.as_view(), name="tool_edit"),
    path("<int:pk>/delete/", ToolDeleteView.as_view(), name="tool_delete"),
]
