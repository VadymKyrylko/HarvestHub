from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .models import User
from .forms import CustomUserCreationForm


def get_redirect_url_by_role(user):
    if user.role == User.Role.ADMIN:
        return reverse("admin:index")
    elif user.role == User.Role.WORKER:
        return reverse("worker_dashboard")
    return reverse("home")


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"

    def get_success_url(self):
        return get_redirect_url_by_role(self.request.user)


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(get_redirect_url_by_role(user))
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})

@login_required
def worker_dashboard(request):
    return render(request, "accounts/worker_dashboard.html")