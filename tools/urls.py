from django.urls import path
from . import views

app_name = "tools"

urlpatterns = [
    path("", views.ToolListView.as_view(), name="tool_list"),
]