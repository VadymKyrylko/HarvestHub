from django.db import models


class Material(models.Model):
    class Unit(models.TextChoices):
        KILOGRAM = "kg", "Kilogram"
        LITER = "l", "Liter"
        PIECE = "pcs", "Piece"

    name = models.CharField(max_length=100, unique=True)
    unit = models.CharField(
        max_length=10,
        choices=Unit.choices,
        help_text="Unit of measurement"
    )

    def __str__(self):
        return f"{self.name} ({self.get_unit_display()})"

    class Meta:
        verbose_name = "Material"
        verbose_name_plural = "Materials"
        ordering = ["name"]