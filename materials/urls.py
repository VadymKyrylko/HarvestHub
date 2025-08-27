from django.urls import path
from . import views
from .views import MaterialCreateView, MaterialUpdateView, MaterialDeleteView

app_name = "materials"

urlpatterns = [
    path("", views.MaterialListView.as_view(), name="material_list"),
    path("add/", MaterialCreateView.as_view(), name="material_add"),
    path("<int:pk>/edit/", MaterialUpdateView.as_view(), name="material_edit"),
    path("<int:pk>/delete/", MaterialDeleteView.as_view(), name="material_delete"),
]