from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from materials.models import Material

User = get_user_model()


class MaterialListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Material.objects.create(name="Sand", unit=Material.Unit.KILOGRAM)
        Material.objects.create(name="Water", unit=Material.Unit.LITER)

    def test_anyone_can_see_materials_list(self):
        resp = self.client.get(reverse("materials:material_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Sand")
        self.assertContains(resp, "Water")


class MaterialDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.material = Material.objects.create(
            name="Bricks", unit=Material.Unit.PIECE
        )

    def test_detail_view_displays_material(self):
        resp = self.client.get(
            reverse(
                "materials:material_detail",
                kwargs={"pk": self.material.pk}
            )
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Bricks")
        self.assertContains(resp, "Piece")


class MaterialCreateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testcreator", password="tpassword"
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse("materials:material_create"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_logged_in_user_can_create(self):
        self.client.login(username="testcreator", password="tpassword")
        resp = self.client.post(
            reverse("materials:material_create"),
            {"name": "Cement", "unit": Material.Unit.KILOGRAM},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Material.objects.filter(name="Cement").exists())


class MaterialUpdateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testupdater", password="tpassword"
        )
        cls.material = Material.objects.create(
            name="Gravel", unit=Material.Unit.KILOGRAM
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(
            reverse(
                "materials:material_update",
                kwargs={"pk": self.material.pk}
            )
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_logged_in_user_can_update(self):
        self.client.login(username="testupdater", password="tpassword")
        resp = self.client.post(
            reverse(
                "materials:material_update",
                kwargs={"pk": self.material.pk}
            ),
            {"name": "UpdatedGravel", "unit": Material.Unit.KILOGRAM},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Material.objects.filter(name="UpdatedGravel").exists())


class MaterialDeleteViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testdeleter", password="tpassword"
        )
        cls.material = Material.objects.create(
            name="Clay",
            unit=Material.Unit.KILOGRAM
        )

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(
            reverse(
                "materials:material_delete", kwargs={"pk": self.material.pk}
            )
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_logged_in_user_can_delete(self):
        self.client.login(username="testdeleter", password="tpassword")
        resp = self.client.post(
            reverse(
                "materials:material_delete", kwargs={"pk": self.material.pk}
            )
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Material.objects.filter(pk=self.material.pk).exists())
