from django import forms
from tools.models import Tool

class ToolForm(forms.ModelForm):
    class Meta:
        model = Tool
        fields = ["name", "status", "is_checked_out"]