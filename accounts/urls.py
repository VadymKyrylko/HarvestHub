from django.urls import path
from .views import register, CustomLoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("auth/register/", register, name="register"),
    path("auth/login/", CustomLoginView.as_view(), name="login"),
    path(
        "auth/logout/",
        LogoutView.as_view(next_page="plants:bed_list"),
        name="logout"
    ),
    path("dashboard/worker/", views.worker_dashboard, name="worker_dashboard"),
]
