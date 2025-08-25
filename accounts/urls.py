from django.urls import path
from .views import register, CustomLoginView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="home"), name="logout"),
    path("worker-dashboard/", views.worker_dashboard, name="worker_dashboard"),
]