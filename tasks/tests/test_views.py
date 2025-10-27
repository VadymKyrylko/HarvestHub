from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import MaintenanceTask

User = get_user_model()


class TaskListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="owner", password="pass")
        cls.other_user = User.objects.create_user(
            username="other", password="pass"
        )
        cls.staff = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        cls.superuser = User.objects.create_user(
            username="root", password="pass", is_superuser=True
        )
        cls.task1 = MaintenanceTask.objects.create(
            name="Owner task",
            scheduled_at=timezone.now(),
            assigned_to=cls.owner
        )
        cls.task2 = MaintenanceTask.objects.create(
            name="Other task",
            scheduled_at=timezone.now(),
            assigned_to=cls.other_user
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("tasks:task_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login", resp.url)

    def test_superuser_sees_all_tasks(self):
        self.client.login(username="root", password="pass")
        resp = self.client.get(reverse("tasks:task_list"))
        self.assertContains(resp, "Owner task")
        self.assertContains(resp, "Other task")

    def test_staff_sees_all_tasks(self):
        self.client.login(username="staff", password="pass")
        resp = self.client.get(reverse("tasks:task_list"))
        self.assertContains(resp, "Owner task")
        self.assertContains(resp, "Other task")

    def test_owner_sees_only_own_tasks(self):
        self.client.login(username="owner", password="pass")
        resp = self.client.get(reverse("tasks:task_list"))
        self.assertContains(resp, "Owner task")
        self.assertNotContains(resp, "Other task")

    def test_other_user_sees_only_their_tasks(self):
        self.client.login(username="other", password="pass")
        resp = self.client.get(reverse("tasks:task_list"))
        self.assertContains(resp, "Other task")
        self.assertNotContains(resp, "Owner task")


class TaskDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_user(username="owner", password="pass")
        cls.other_user = User.objects.create_user(
            username="other", password="pass"
        )
        cls.staff = User.objects.create_user(
            username="staff", password="pass", is_staff=True
        )
        cls.superuser = User.objects.create_user(
            username="root", password="pass", is_superuser=True
        )

        cls.task = MaintenanceTask.objects.create(
            name="Owner task",
            scheduled_at=timezone.now(),
            assigned_to=cls.owner
        )

    def test_superuser_can_access_any_task(self):
        self.client.login(username="root", password="pass")
        resp = self.client.get(
            reverse("tasks:task_detail", args=[self.task.pk])
        )
        self.assertEqual(resp.status_code, 200)

    def test_staff_can_access_any_task(self):
        self.client.login(username="staff", password="pass")
        resp = self.client.get(
            reverse("tasks:task_detail", args=[self.task.pk])
        )
        self.assertEqual(resp.status_code, 200)

    def test_owner_can_access_own_task(self):
        self.client.login(username="owner", password="pass")
        resp = self.client.get(
            reverse("tasks:task_detail", args=[self.task.pk])
        )
        self.assertEqual(resp.status_code, 200)

    def test_other_user_gets_403(self):
        self.client.login(username="other", password="pass")
        resp = self.client.get(
            reverse("tasks:task_detail", args=[self.task.pk])
        )
        self.assertEqual(resp.status_code, 403)
