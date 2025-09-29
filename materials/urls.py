from django.urls import path
from . import views
from .views import (
    MaterialCreateView,
    MaterialUpdateView,
    MaterialDeleteView,
    MaterialDetailView,
)

app_name = "materials"

urlpatterns = [
    path(
        "",
        views.MaterialListView.as_view(),
        name="material_list"),
    path(
        "new/",
        MaterialCreateView.as_view(),
        name="material_create"),
    path(
        "<int:pk>/",
        MaterialDetailView.as_view(),
        name="material_detail"),
    path(
        "<int:pk>/update/",
        MaterialUpdateView.as_view(),
        name="material_update"),
    path(
        "<int:pk>/delete/",
        MaterialDeleteView.as_view(),
        name="material_delete"
    ),
]
