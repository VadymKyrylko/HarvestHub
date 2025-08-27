import django_filters
from .models import MaintenanceTask

class MaintenanceTaskFilter(django_filters.FilterSet):
    scheduled_at__gte = django_filters.DateFilter(
        field_name="scheduled_at",
        lookup_expr="gte",
        label="Date from"
    )
    scheduled_at__lte = django_filters.DateFilter(
        field_name="scheduled_at",
        lookup_expr="lte",
        label="Date to"
    )

    class Meta:
        model = MaintenanceTask
        fields = ["status", "assigned_to"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.form.fields["scheduled_at__gte"].widget.attrs.update({
            "type": "date",
            "class": "form-control"
        })
        self.form.fields["scheduled_at__lte"].widget.attrs.update({
            "type": "date",
            "class": "form-control"
        })

        self.form.fields["status"].widget.attrs.update({"class": "form-control"})
        self.form.fields["assigned_to"].widget.attrs.update({"class": "form-control"})