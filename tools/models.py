from django.db import models


class Tool(models.Model):
    class ToolStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        IN_USE = "IN_USE", "In use"
        BROKEN = "BROKEN", "Broken"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=20,
        choices=ToolStatus.choices,
        default=ToolStatus.AVAILABLE
    )
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    class Meta:
        verbose_name = "Tool"
        verbose_name_plural = "Tools"
        ordering = ["name"]