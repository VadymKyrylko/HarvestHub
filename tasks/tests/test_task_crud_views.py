from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import MaintenanceTask

User = get_user_model()


class TaskCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="user", password="pass")

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("tasks:task_create"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.url)

    def test_logged_in_user_can_create_task(self):
        self.client.login(username="user", password="pass")
        resp = self.client.post(reverse("tasks:task_create"), {
            "name": "New Task",
            "scheduled_at": timezone.now(),
            "status": MaintenanceTask.TaskStatus.PLANNED
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(MaintenanceTask.objects.filter(name="New Task").exists())


class TaskUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="owner", password="pass")
        cls.other_user = User.objects.create_user(username="other", password="pass")
        cls.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
        cls.superuser = User.objects.create_user(username="root", password="pass", is_superuser=True)

        cls.task = MaintenanceTask.objects.create(
            name="Owner task",
            scheduled_at=timezone.now(),
            assigned_to=cls.owner
        )

    def test_owner_can_update(self):
        self.client.login(username="owner", password="pass")
        resp = self.client.post(reverse("tasks:task_update", args=[self.task.pk]), {
            "name": "Updated Task",
            "scheduled_at": timezone.now(),
            "status": MaintenanceTask.TaskStatus.PLANNED
        })
        self.assertEqual(resp.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Updated Task")

    def test_staff_can_update(self):
        self.client.login(username="staff", password="pass")
        resp = self.client.post(reverse("tasks:task_update", args=[self.task.pk]), {
            "name": "Staff Updated",
            "scheduled_at": timezone.now(),
            "status": MaintenanceTask.TaskStatus.PLANNED
        })
        self.assertEqual(resp.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Staff Updated")

    def test_superuser_can_update(self):
        self.client.login(username="root", password="pass")
        resp = self.client.post(reverse("tasks:task_update", args=[self.task.pk]), {
            "name": "Root Updated",
            "scheduled_at": timezone.now(),
            "status": MaintenanceTask.TaskStatus.PLANNED
        })
        self.assertEqual(resp.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, "Root Updated")

    def test_other_user_cannot_update(self):
        self.client.login(username="other", password="pass")
        resp = self.client.post(reverse("tasks:task_update", args=[self.task.pk]), {
            "name": "Hacked",
            "scheduled_at": timezone.now(),
            "status": MaintenanceTask.TaskStatus.PLANNED
        })
        self.assertIn(resp.status_code, [403, 404])
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.name, "Hacked")


class TaskDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="owner", password="pass")
        cls.other_user = User.objects.create_user(username="other", password="pass")
        cls.staff = User.objects.create_user(username="staff", password="pass", is_staff=True)
        cls.superuser = User.objects.create_user(username="root", password="pass", is_superuser=True)

        cls.task = MaintenanceTask.objects.create(
            name="Owner task",
            scheduled_at=timezone.now(),
            assigned_to=cls.owner
        )

    def test_owner_can_delete(self):
        self.client.login(username="owner", password="pass")
        resp = self.client.post(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(MaintenanceTask.objects.filter(pk=self.task.pk).exists())

    def test_staff_can_delete(self):
        self.client.login(username="staff", password="pass")
        resp = self.client.post(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(MaintenanceTask.objects.filter(pk=self.task.pk).exists())

    def test_superuser_can_delete(self):
        self.client.login(username="root", password="pass")
        resp = self.client.post(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(MaintenanceTask.objects.filter(pk=self.task.pk).exists())

    def test_other_user_cannot_delete(self):
        self.client.login(username="other", password="pass")
        resp = self.client.post(reverse("tasks:task_delete", args=[self.task.pk]))
        self.assertIn(resp.status_code, [403, 404])
        self.assertTrue(MaintenanceTask.objects.filter(pk=self.task.pk).exists())
