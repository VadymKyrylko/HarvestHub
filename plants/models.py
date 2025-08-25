from django.core.exceptions import ValidationError
from django.db import models

class GardenBed(models.Model):
    name = models.CharField(max_length=100)
    length = models.DecimalField(max_digits=5, decimal_places=2)  # m
    width = models.DecimalField(max_digits=5, decimal_places=2)   # m

    @property
    def area(self):
        return self.length * self.width  # m²


class Plant(models.Model):
    name = models.CharField(max_length=100)
    space_per_plant = models.DecimalField(
        max_digits=5, decimal_places=2,
        help_text="Required area for one plant, m²"
    )


class BedSection(models.Model):
    bed = models.ForeignKey(GardenBed, on_delete=models.CASCADE, related_name="sections")
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    plant_count = models.PositiveIntegerField()
    length = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    @property
    def allocated_area(self):
        if self.length and self.width:
            return self.length * self.width
        return None

    @property
    def required_area(self):
        return self.plant_count * self.plant.space_per_plant

    def clean(self):
        if self.required_area > self.bed.area:
            raise ValidationError(
                f"Not enough area: need {self.required_area} m², "
                f"and the bed has only {self.bed.area} m²."
            )