from django.core.exceptions import ValidationError
from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from plants.models import GardenBed
from tools.models import Tool
from materials.models import Material


class MaintenanceTask(models.Model):
    class TaskStatus(models.TextChoices):
        PLANNED = "PLANNED", "Planned"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        DONE = "DONE", "Done"

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    scheduled_at = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.PLANNED
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="tasks"
    )

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

    class Meta:
        verbose_name = "Maintenance task"
        verbose_name_plural = "Maintenance tasks"
        ordering = ["-scheduled_at"]

    def clean(self):
        super().clean()
        if not self.pk:
            return
        if self.status == self.TaskStatus.IN_PROGRESS:
            for task_tool in self.tools_used.select_related("tool"):
                tool = task_tool.tool
                conflict_exists = (
                    tool.task_tools
                    .exclude(task=self)
                    .filter(task__status=self.TaskStatus.IN_PROGRESS)
                    .exists()
                )
                if conflict_exists or tool.status == tool.ToolStatus.IN_USE:
                    raise ValidationError(
                        f"Tool '{tool.name}' "
                        f"already used in another active task."
                    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class GardenBedTask(models.Model):
    bed = models.ForeignKey(
        GardenBed,
        on_delete=models.CASCADE,
        related_name="bed_tasks"
    )
    task = models.ForeignKey(
        MaintenanceTask,
        on_delete=models.CASCADE,
        related_name="bed_tasks"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["bed", "task"],
                name="unique_bed_per_task"
            )
        ]

    def __str__(self):
        return f"Task: {self.task.name} -> Bed: {self.bed.name}"


class MaterialUsage(models.Model):
    task = models.ForeignKey(
        MaintenanceTask,
        on_delete=models.CASCADE,
        related_name="materials_used"
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        related_name="usages"
    )
    quantity_used = models.DecimalField(
        max_digits=7, decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "material"],
                name="unique_material_per_task"
            )
        ]

    def __str__(self):
        return (f"{self.material.name}: "
                f"{self.quantity_used} "
                f"{self.material.unit}")


class TaskTool(models.Model):
    task = models.ForeignKey(
        MaintenanceTask,
        on_delete=models.CASCADE,
        related_name="tools_used"
    )
    tool = models.ForeignKey(
        Tool,
        on_delete=models.CASCADE,
        related_name="task_tools"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task", "tool"],
                name="unique_tool_per_task"
            )
        ]

    def clean(self):
        super().clean()
        conflict_exists = self.tool.task_tools.filter(
            task__status=MaintenanceTask.TaskStatus.IN_PROGRESS
        ).exclude(task=self.task).exists()

        if conflict_exists:
            raise ValidationError(
                f"The «{self.tool.name}» already used in another active task."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tool.name} for {self.task.name}"
