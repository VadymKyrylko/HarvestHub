from django import forms
from .models import MaintenanceTask, GardenBedTask, MaterialUsage, TaskTool

class MaintenanceTaskForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTask
        fields = ["name", "description", "scheduled_at", "status", "assigned_to"]

class GardenBedTaskForm(forms.ModelForm):
    class Meta:
        model = GardenBedTask
        fields = ["bed", "task"]

class MaterialUsageForm(forms.ModelForm):
    class Meta:
        model = MaterialUsage
        fields = ["task", "material", "quantity_used"]

class TaskToolForm(forms.ModelForm):
    class Meta:
        model = TaskTool
        fields = ["task", "tool"]

