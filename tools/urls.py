from django.urls import path
from . import views
from .views import ToolCreateView, ToolUpdateView, ToolDeleteView, ToolDetailView

app_name = "tools"

urlpatterns = [
    path("", views.ToolListView.as_view(), name="tool_list"),
    path("new/", ToolCreateView.as_view(), name="tool_create"),
    path("<int:pk>/", ToolDetailView.as_view(), name="tool_detail"),
    path("<int:pk>/edit/", ToolUpdateView.as_view(), name="tool_update"),
    path("<int:pk>/delete/", ToolDeleteView.as_view(), name="tool_delete"),
]
