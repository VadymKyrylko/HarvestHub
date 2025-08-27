from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

class GardenBed(models.Model):
    name = models.CharField(max_length=100)
    length = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.1)])  # m
    width = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.1)])   # m
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Garden bed"
        verbose_name_plural = "Garden beds"
        ordering = ["name"]


    @property
    def area(self):
        return self.length * self.width  # m²

    def __str__(self):
        return self.name

class Plant(models.Model):

    class PlantType(models.TextChoices):
        VEGETABLE = "VEG", "Vegetable"
        HERB = "HERB", "Herb"
        BERRY = "BERRY", "Berry"
        FLOWER = "FLOWER", "Flower"

    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"
        ordering = ["name"]

    name = models.CharField(max_length=100)
    plant_type = models.CharField(
        max_length=10,
        choices=PlantType.choices,
        default=PlantType.VEGETABLE
    )
    space_per_plant = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Required area for one plant, m²"
    )


    def __str__(self):
        return f"{self.name} ({self.get_plant_type_display()})"


class BedSection(models.Model):
    bed = models.ForeignKey(GardenBed, on_delete=models.CASCADE, related_name="sections")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, null=True, blank=True, related_name="sections")
    plant_count = models.PositiveIntegerField()
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.1)])
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, validators=[MinValueValidator(0.1)])

    @property
    def allocated_area(self):
        if self.length and self.width:
            return self.length * self.width
        return None

    @property
    def required_area(self):
        if not self.plant:
            return 0
        return self.plant_count * self.plant.space_per_plant

    def clean(self):
        if self.required_area > self.bed.area:
            raise ValidationError(
                f"Not enough area: need {self.required_area} m², "
                f"and the bed has only {self.bed.area} m²."
            )

    class Meta:
        verbose_name = "Bed Section"
        verbose_name_plural = "Bed Sections"
        ordering = ["bed", "plant"]

    def __str__(self):
        return f"{self.bed.name} - {self.plant.name if self.plant else 'Empty'}"