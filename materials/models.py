from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(
        max_length=20,
        help_text="Unit of measurement (e.g. kg, l, pcs)"
    )

    def __str__(self):
        return f"{self.name} ({self.unit})"

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        ordering = ["name"]
