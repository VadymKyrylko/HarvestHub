from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Tool
from .forms import ToolForm

class ToolListView(ListView):
    model = Tool
    template_name = "tools/tool_list.html"
    context_object_name = "tools"

class ToolCreateView(CreateView):
    model = Tool
    form_class = ToolForm
    template_name = "tools/tool_form.html"
    success_url = reverse_lazy("tools:tool_list")

class ToolUpdateView(UpdateView):
    model = Tool
    form_class = ToolForm
    template_name = "tools/tool_form.html"
    success_url = reverse_lazy("tools:tool_list")

class ToolDeleteView(DeleteView):
    model = Tool
    template_name = "tools/tool_confirm_delete.html"
    success_url = reverse_lazy("tools:tool_list")