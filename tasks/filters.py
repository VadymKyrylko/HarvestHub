import django_filters
from .models import MaintenanceTask
from .forms import MaintenanceTaskFilterForm

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
        form = MaintenanceTaskFilterForm
