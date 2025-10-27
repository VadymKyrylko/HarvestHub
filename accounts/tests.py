from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import SESSION_KEY

from accounts.forms import CustomUserCreationForm

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_defaults_to_worker(self):
        user = User.objects.create_user(username="worker1", password="pass123")
        self.assertEqual(user.role, User.Role.WORKER)
        self.assertTrue(user.check_password("pass123"))

    def test_create_superuser_has_admin_role(self):
        admin = User.objects.create_superuser(
            username="admin1", password="adminpass"
        )
        self.assertEqual(admin.role, User.Role.ADMIN)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_str_representation(self):
        user = User.objects.create_user(username="john", password="pass")
        self.assertIn("john", str(user))
        self.assertIn("Worker", str(user))


class CustomUserCreationFormTests(TestCase):
    def test_form_creates_worker_user(self):
        form = CustomUserCreationForm(
            data={
                "username": "newuser",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.role, User.Role.WORKER)


class RegisterViewTests(TestCase):
    def test_get_register_page(self):
        resp = self.client.get(reverse("register"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "<form")

    def test_post_register_creates_and_logs_in_user(self):
        resp = self.client.post(
            reverse("register"),
            {
                "username": "registeruser",
                "password1": "StrongPass123",
                "password2": "StrongPass123",
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(User.objects.filter(username="registeruser").exists())
        self.assertIn(SESSION_KEY, self.client.session)


class LoginViewTests(TestCase):
    def setUp(self):
        self.worker = User.objects.create_user(
            username="worker", password="pass123"
        )
        self.admin = User.objects.create_superuser(
            username="admin", password="adminpass"
        )

    def test_worker_redirects_to_dashboard(self):
        resp = self.client.post(
            reverse("login"), {"username": "worker", "password": "pass123"}
        )
        self.assertRedirects(resp, reverse("worker_dashboard"))

    def test_admin_redirects_to_admin_index(self):
        resp = self.client.post(
            reverse("login"), {"username": "admin", "password": "adminpass"}
        )
        self.assertRedirects(resp, reverse("admin:index"))


class WorkerDashboardTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="dashboarduser", password="pass123"
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("worker_dashboard"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/auth/login/", resp.url)

    def test_logged_in_user_can_access(self):
        self.client.login(username="dashboarduser", password="pass123")
        resp = self.client.get(reverse("worker_dashboard"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "dashboard")


class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="logoutuser", password="pass123"
        )

    def test_logout_redirects_to_bed_list(self):
        self.client.login(username="logoutuser", password="pass123")
        resp = self.client.post(reverse("logout"))
        self.assertRedirects(resp, reverse("plants:bed_list"))
