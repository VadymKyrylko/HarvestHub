from django import forms
from tasks.models import (
    MaintenanceTask,
    GardenBedTask,
    MaterialUsage,
    TaskTool,
    Tool
)
from django.core.exceptions import ValidationError


class BootstrapModelForm(forms.ModelForm):
    """
    Base form with auto add
    Bootstrap class 'form-control' and error highlight
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            existing_classes = field.widget.attrs.get("class", "")
            css_classes = existing_classes + " form-control"

            if self.errors.get(name):
                css_classes += " is-invalid"
            field.widget.attrs["class"] = css_classes.strip()


class MaintenanceTaskForm(BootstrapModelForm):
    class Meta:
        model = MaintenanceTask
        fields = [
            "name",
            "description",
            "status",
            "scheduled_at",
            "assigned_to"
        ]
        widgets = {
            "scheduled_at": forms.DateTimeInput(attrs={
                "type": "datetime-local",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial = dict(self.initial)
        if self.instance and self.instance.scheduled_at:
            self.initial["scheduled_at"] = (
                self.instance.scheduled_at.strftime("%Y-%m-%dT%H:%M")
            )


class GardenBedTaskForm(BootstrapModelForm):
    class Meta:
        model = GardenBedTask
        fields = ["bed", "task"]

    def clean(self):
        cleaned_data = super().clean()
        bed = cleaned_data.get("bed")
        task = cleaned_data.get("task")
        if bed and task:
            exists = GardenBedTask.objects.filter(bed=bed, task=task)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError(
                    "This bed has already been added to this task."
                )
        return cleaned_data


class MaterialUsageForm(BootstrapModelForm):
    class Meta:
        model = MaterialUsage
        fields = ["task", "material", "quantity_used"]

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get("task")
        material = cleaned_data.get("material")
        if task and material:
            exists = MaterialUsage.objects.filter(task=task, material=material)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError(
                    "This material is already used in this task."
                )
        return cleaned_data


class TaskToolForm(BootstrapModelForm):
    class Meta:
        model = TaskTool
        fields = ["task", "tool"]

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get("task")
        tool = cleaned_data.get("tool")

        if task and tool:
            exists = TaskTool.objects.filter(task=task, tool=tool)
            if self.instance.pk:
                exists = exists.exclude(pk=self.instance.pk)
            if exists.exists():
                raise ValidationError(
                    "This tool is already used in this task."
                )

            conflict_exists = (
                tool.task_tools.exclude(
                    task=task
                ).filter(
                    task__status=MaintenanceTask.TaskStatus.IN_PROGRESS
                ).exists()
            )
            if conflict_exists or tool.status == Tool.ToolStatus.IN_USE:
                raise ValidationError(
                    f"The «{tool.name}» already used in another active task."
                )

        return cleaned_data
