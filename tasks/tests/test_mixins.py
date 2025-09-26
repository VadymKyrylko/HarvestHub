from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import MaintenanceTask

User = get_user_model()


@override_settings(ROOT_URLCONF="tasks.tests.test_urls")
class TaskObjectPermissionMixinTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regular_user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        cls.staff = User.objects.create_user(
            username="teststaff", password="stafftestpass", is_staff=True
        )
        cls.superuser = User.objects.create_user(
            username="testadmin", password="testadminpass", is_superuser=True
        )
        cls.task = MaintenanceTask.objects.create(
            name="Test task",
            scheduled_at=timezone.now(),
            assigned_to=cls.regular_user
        )

    def test_superuser_has_access(self):
        self.client.login(username="testadmin", password="testadminpass")
        resp = self.client.get(reverse("dummy_task", args=[self.task.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_staff_has_access(self):
        self.client.login(username="teststaff", password="stafftestpass")
        resp = self.client.get(reverse("dummy_task", args=[self.task.pk]))
        self.assertEqual(resp.status_code, 200)

    def test_owner_has_access(self):
        self.client.login(username="testuser", password="testpass")
        resp = self.client.get(reverse("dummy_task", args=[self.task.pk]))
        self.assertEqual(resp.status_code, 200)


@override_settings(ROOT_URLCONF="tasks.tests.test_urls")
class RelatedTaskPermissionMixinTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regular_user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        cls.staff = User.objects.create_user(
            username="teststaff", password="stafftestpass", is_staff=True
        )
        cls.superuser = User.objects.create_user(
            username="testadmin", password="testadminpass", is_superuser=True
        )
        cls.task = MaintenanceTask.objects.create(
            name="Test task",
            scheduled_at=timezone.now(),
            assigned_to=cls.regular_user
        )

    def test_superuser_can_access_with_task_param(self):
        self.client.login(username="testadmin", password="testadminpass")
        resp = self.client.get(reverse("dummy_related") + f"?task={self.task.pk}")
        self.assertEqual(resp.status_code, 200)

    def test_staff_can_access_with_task_param(self):
        self.client.login(username="teststaff", password="stafftestpass")
        resp = self.client.get(reverse("dummy_related") + f"?task={self.task.pk}")
        self.assertEqual(resp.status_code, 200)

    def test_owner_can_access_with_task_param(self):
        self.client.login(username="testuser", password="testpass")
        resp = self.client.get(reverse("dummy_related") + f"?task={self.task.pk}")
        self.assertEqual(resp.status_code, 200)

    def test_task_not_found_returns_404(self):
        self.client.login(username="testadmin", password="testadminpass")
        resp = self.client.get(reverse("dummy_related") + "?task=9999")
        self.assertEqual(resp.status_code, 404)