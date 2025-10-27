from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from tasks.models import MaintenanceTask, TaskTool
from tools.models import Tool

User = get_user_model()


class ToolListViewTests(TestCase):
    def test_anyone_can_see_tools_list(self):
        resp = self.client.get(reverse("tools:tool_list"))
        self.assertEqual(200, resp.status_code)


class ToolDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="test_user",
            password="test_pass"
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("tools:tool_detail", kwargs={"pk": 1}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)


class ToolCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpass"
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("tools:tool_create"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_logged_in_user_can_create(self):
        self.client.login(username="testuser", password="testpass")
        resp = self.client.post(
            reverse("tools:tool_create"),
            {
                "name": "Tool1",
                "status": Tool.ToolStatus.AVAILABLE,
                "is_checked_out": False,
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Tool.objects.filter(name="Tool1").exists())


class ToolUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser1",
            password="testpass"
        )
        cls.tool = Tool.objects.create(name="UpdatedTool")

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(
            reverse("tools:tool_update", kwargs={"pk": self.tool.pk})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_logged_in_user_can_update(self):
        self.client.login(username="testuser1", password="testpass")
        resp = self.client.post(
            reverse("tools:tool_update", kwargs={"pk": self.tool.pk}),
            {
                "name": "UpdatedTool",
                "status": Tool.ToolStatus.AVAILABLE,
                "is_checked_out": False,
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Tool.objects.filter(name=self.tool.name).exists())


class ToolDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser2",
            password="testpass"
        )
        cls.tool = Tool.objects.create(name="DeletedTool")

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(
            reverse("tools:tool_delete", kwargs={"pk": self.tool.pk})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_logged_in_user_can_delete(self):
        self.client.login(username="testuser2", password="testpass")
        resp = self.client.post(
            reverse("tools:tool_delete", kwargs={"pk": self.tool.pk}),
            {"name": self.tool.name},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Tool.objects.filter(name=self.tool.name).exists())


class TaskToolViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser3",
            password="testpass"
        )
        cls.task = MaintenanceTask.objects.create(
            name="Task1",
            scheduled_at=timezone.now(),
            assigned_to=cls.user,
            status=MaintenanceTask.TaskStatus.PLANNED,
        )
        cls.tool = Tool.objects.create(
            name="Tool1",
        )

    def test_can_create_tasktool_for_non_active_task(self):
        self.client.login(username="testuser3", password="testpass")
        resp = self.client.post(
            reverse("tasks:tasktool_create", kwargs={"task_id": self.task.id}),
            {"tool": self.tool.id},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            TaskTool.objects.filter(task=self.task, tool=self.tool).exists()
        )

    def test_tool_binding_to_the_task(self):
        self.client.login(username="testuser3", password="testpass")
        resp = self.client.post(
            reverse("tasks:tasktool_create", kwargs={"task_id": self.task.id}),
            {"tool": self.tool.id},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            TaskTool.objects.filter(task=self.task, tool=self.tool).exists()
        )

    def test_count_of_tasktool_raises_after_creating_new_one(self):
        self.client.login(username="testuser3", password="testpass")
        count_before = TaskTool.objects.count()
        resp = self.client.post(
            reverse("tasks:tasktool_create", kwargs={"task_id": self.task.id}),
            {"tool": self.tool.id},
        )
        count_after = TaskTool.objects.count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count_after, count_before + 1)


class TaskToolNegativeViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser4",
            password="pass4"
        )
        cls.task = MaintenanceTask.objects.create(
            name="Task2",
            scheduled_at=timezone.now(),
            assigned_to=cls.user,
            status=MaintenanceTask.TaskStatus.PLANNED,
        )
        cls.tool = Tool.objects.create(
            name="Tool2",
        )

    def test_redirect_if_not_logged_in(self):
        count_before = TaskTool.objects.count()
        resp = self.client.get(
            reverse("tasks:tasktool_create", kwargs={"task_id": self.task.id})
        )
        count_after = TaskTool.objects.count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(count_after, count_before)
        self.assertIn("/login", resp.url)

    def test_cannot_create_identical_tasktool(self):
        self.client.login(username="testuser4", password="pass4")
        count_before_first_creation = TaskTool.objects.count()
        resp = self.client.post(
            reverse("tasks:tasktool_create", kwargs={"task_id": self.task.id}),
            {"tool": self.tool.id},
        )
        count_after_first_creation = TaskTool.objects.count()
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(
            count_after_first_creation,
            count_before_first_creation + 1
        )
        count_before_second_creation = TaskTool.objects.count()
        with self.assertRaises(ValidationError):
            self.client.post(
                reverse(
                    "tasks:tasktool_create",
                    kwargs={"task_id": self.task.id}
                ),
                {"tool": self.tool.id},
            )
        count_after_second_creation = TaskTool.objects.count()
        self.assertEqual(
            count_after_second_creation,
            count_before_second_creation
        )

    def test_cannot_use_tool_in_two_active_tasks(self):
        self.client.login(username="testuser4", password="pass4")
        self.task1 = MaintenanceTask.objects.create(
            name="Task3",
            scheduled_at=timezone.now(),
            assigned_to=self.user,
            status=MaintenanceTask.TaskStatus.IN_PROGRESS,
        )
        self.tool = Tool.objects.create(name="Tool3")
        count_before = TaskTool.objects.count()
        resp1 = self.client.post(
            reverse(
                "tasks:tasktool_create",
                kwargs={"task_id": self.task1.id}
            ),
            {"tool": self.tool.id},
        )
        count_after = TaskTool.objects.count()
        self.assertEqual(resp1.status_code, 302)
        self.assertEqual(count_after, count_before + 1)

        self.task2 = MaintenanceTask.objects.create(
            name="Task4",
            scheduled_at=timezone.now(),
            assigned_to=self.user,
            status=MaintenanceTask.TaskStatus.IN_PROGRESS,
        )
        count_before_second = TaskTool.objects.count()
        resp2 = self.client.post(
            reverse(
                "tasks:tasktool_create",
                kwargs={"task_id": self.task2.id}
            ),
            {"tool": self.tool.id},
        )
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, "already used in another active task")
        form = resp2.context["form"]
        self.assertIn(
            "already used in another active task",
            " ".join(form.non_field_errors())
        )
        count_after_second = TaskTool.objects.count()
        self.assertEqual(count_after_second, count_before_second)
