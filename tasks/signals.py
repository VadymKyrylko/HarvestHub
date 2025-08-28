from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MaintenanceTask
from tools.models import Tool


@receiver(post_save, sender=MaintenanceTask)
def update_tools_after_status_change(sender, instance, **kwargs):
    """
    After saving the task:
    If the status is IN_PROGRESS → the tools become IN_USE
    If the status is DONE → the tools become AVAILABLE
    """
    for tt in instance.tools_used.select_related('tool'):
        tool = tt.tool
        if instance.status == MaintenanceTask.TaskStatus.IN_PROGRESS:
            tool.status = Tool.ToolStatus.IN_USE
            tool.is_checked_out = True
        elif instance.status == MaintenanceTask.TaskStatus.DONE:
            tool.status = Tool.ToolStatus.AVAILABLE
            tool.is_checked_out = False
        tool.save()
