from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from plants.forms import BedSectionForm
from plants.models import GardenBed, Plant, BedSection

User = get_user_model()


class GardenBedListViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        GardenBed.objects.create(name="Bed A", length=2, width=3)
        GardenBed.objects.create(name="Bed B", length=1, width=1)

    def test_anyone_can_see_beds_list(self):
        resp = self.client.get(reverse("plants:bed_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Bed A")
        self.assertContains(resp, "Bed B")


class GardenBedDetailViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.bed = GardenBed.objects.create(name="Bed C", length=2, width=2)

    def test_detail_view_displays_bed(self):
        resp = self.client.get(
            reverse("plants:bed_detail", kwargs={"pk": self.bed.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Bed C")
        self.assertContains(resp, "4")


class GardenBedCreateUpdateDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="gardener", password="pass"
        )
        cls.bed = GardenBed.objects.create(name="Bed D", length=1, width=1)

    def test_logged_in_user_can_create_bed(self):
        self.client.login(username="gardener", password="pass")
        resp = self.client.post(
            reverse("plants:bed_create"),
            {"name": "Bed E", "length": 2, "width": 3},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(GardenBed.objects.filter(name="Bed E").exists())

    def test_logged_in_user_can_update_bed(self):
        self.client.login(username="gardener", password="pass")
        resp = self.client.post(
            reverse("plants:bed_update", kwargs={"pk": self.bed.pk}),
            {"name": "Updated Bed D", "length": 1, "width": 2},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(GardenBed.objects.filter(
            name="Updated Bed D"
        ).exists())

    def test_logged_in_user_can_delete_bed(self):
        self.client.login(username="gardener", password="pass")
        resp = self.client.post(
            reverse("plants:bed_delete", kwargs={"pk": self.bed.pk})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(GardenBed.objects.filter(pk=self.bed.pk).exists())


class PlantListDetailTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.plant = Plant.objects.create(
            name="Tomato",
            plant_type=Plant.PlantType.VEGETABLE,
            space_per_plant=0.5
        )

    def test_anyone_can_see_plants_list(self):
        resp = self.client.get(reverse("plants:plant_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Tomato")

    def test_detail_view_displays_plant(self):
        resp = self.client.get(
            reverse("plants:plant_detail", kwargs={"pk": self.plant.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Tomato")
        self.assertContains(resp, "Vegetable")


class PlantCreateUpdateDeleteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="planter", password="pass"
        )
        cls.plant = Plant.objects.create(
            name="Cucumber",
            plant_type=Plant.PlantType.VEGETABLE,
            space_per_plant=0.3
        )

    def test_logged_in_user_can_create_plant(self):
        self.client.login(username="planter", password="pass")
        resp = self.client.post(
            reverse("plants:plant_create"),
            {
                "name": "Rose",
                "plant_type": Plant.PlantType.FLOWER,
                "space_per_plant": 0.2,
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Plant.objects.filter(name="Rose").exists())

    def test_logged_in_user_can_update_plant(self):
        self.client.login(username="planter", password="pass")
        resp = self.client.post(
            reverse("plants:plant_update", kwargs={"pk": self.plant.pk}),
            {
                "name": "Updated Cucumber",
                "plant_type": Plant.PlantType.VEGETABLE,
                "space_per_plant": 0.4,
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Plant.objects.filter(name="Updated Cucumber").exists())

    def test_logged_in_user_can_delete_plant(self):
        self.client.login(username="planter", password="pass")
        resp = self.client.post(
            reverse("plants:plant_delete", kwargs={"pk": self.plant.pk})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(Plant.objects.filter(pk=self.plant.pk).exists())


class BedSectionModelTests(TestCase):
    def test_cannot_exceed_bed_area(self):
        bed = GardenBed.objects.create(name="Small Bed", length=1, width=1)
        plant = Plant.objects.create(
            name="Pumpkin",
            plant_type=Plant.PlantType.VEGETABLE,
            space_per_plant=2
        )
        section = BedSection(bed=bed, plant=plant, plant_count=1)
        with self.assertRaises(ValidationError):
            section.full_clean()

    def test_allocated_and_required_area(self):
        bed = GardenBed.objects.create(name="Bed", length=2, width=2)
        plant = Plant.objects.create(
            name="Lettuce",
            plant_type=Plant.PlantType.VEGETABLE,
            space_per_plant=0.5
        )
        section = BedSection.objects.create(
            bed=bed, plant=plant, plant_count=2, length=1, width=1
        )
        self.assertEqual(section.allocated_area, 1)
        self.assertEqual(section.required_area, 1)


class BedSectionFormTests(TestCase):
    def setUp(self):
        self.bed = GardenBed.objects.create(name="Form Bed", length=2, width=2)
        self.plant = Plant.objects.create(
            name="Carrot",
            plant_type=Plant.PlantType.VEGETABLE,
            space_per_plant=0.2
        )

    def test_valid_form_within_capacity(self):
        form = BedSectionForm(
            data={
                "bed": self.bed.id,
                "plant": self.plant.id,
                "plant_count": 3,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_exceed_capacity_raises_error(self):
        BedSection.objects.create(
            bed=self.bed, plant=self.plant, plant_count=3
        )
        form = BedSectionForm(
            data={
                "bed": self.bed.id,
                "plant": self.plant.id,
                "plant_count": 2,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("exceed the bed capacity", str(form.errors))

    def test_update_section_does_not_double_count(self):
        section = BedSection.objects.create(
            bed=self.bed, plant=self.plant, plant_count=2
        )
        form = BedSectionForm(
            data={
                "bed": self.bed.id,
                "plant": self.plant.id,
                "plant_count": 3,
            },
            instance=section,
        )
        self.assertTrue(form.is_valid(), form.errors)


class BedSectionViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="sectioner", password="pass"
        )
        cls.bed = GardenBed.objects.create(name="Bed X", length=3, width=3)
        cls.plant = Plant.objects.create(
            name="Carrot",
            plant_type=Plant.PlantType.VEGETABLE,
            space_per_plant=0.2
        )
        cls.section = BedSection.objects.create(
            bed=cls.bed, plant=cls.plant, plant_count=5
        )

    def test_list_view(self):
        resp = self.client.get(reverse("plants:section_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Carrot")

    def test_detail_view(self):
        resp = self.client.get(
            reverse("plants:section_detail", kwargs={"pk": self.section.pk})
        )
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Carrot")

    def test_logged_in_user_can_create_section(self):
        self.client.login(username="sectioner", password="pass")
        resp = self.client.post(
            reverse("plants:section_create"),
            {"bed": self.bed.pk, "plant": self.plant.pk, "plant_count": 3},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            BedSection.objects.filter(
                bed=self.bed, plant=self.plant, plant_count=3
            ).exists()
        )

    def test_logged_in_user_can_update_section(self):
        self.client.login(username="sectioner", password="pass")
        resp = self.client.post(
            reverse("plants:section_update", kwargs={"pk": self.section.pk}),
            {"bed": self.bed.pk, "plant": self.plant.pk, "plant_count": 10},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            BedSection.objects.filter(
                pk=self.section.pk,
                plant_count=10
            ).exists()
        )

    def test_logged_in_user_can_delete_section(self):
        self.client.login(username="sectioner", password="pass")
        resp = self.client.post(
            reverse("plants:section_delete", kwargs={"pk": self.section.pk})
        )
        self.assertEqual(resp.status_code, 302)
        self.assertFalse(BedSection.objects.filter(
            pk=self.section.pk
        ).exists())
