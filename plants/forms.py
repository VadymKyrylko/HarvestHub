from django import forms
from .models import BedSection

class BedSectionForm(forms.ModelForm):
    class Meta:
        model = BedSection
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        bed = cleaned_data.get("bed")
        plants_in_new_section = cleaned_data.get("plants_count")

        if bed and plants_in_new_section is not None:
            total_existing = BedSection.objects.filter(bed=bed).aggregate(
                total=forms.models.Sum("plants_count")
            )["total"] or 0

            if self.instance.pk:
                total_existing -= self.instance.plants_count or 0

            total_after_add = total_existing + plants_in_new_section

            if total_after_add > bed.capacity:
                raise forms.ValidationError(
                    f"Adding this section will exceed the bed capacity "
                    f"({bed.capacity} of plants). It will be {total_after_add}."
                )

        return cleaned_data