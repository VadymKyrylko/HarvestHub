from django.db import models

class Plant(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class GardenBed(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Gardenbed #{self.id} — {self.plant.name}"