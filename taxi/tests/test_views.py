from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Manufacturer

MANUFACTURER_URL = reverse("taxi:manufacturer-list")


class PublicManufacturerTest(TestCase):
    def test_login_required(self):
        response = self.client.get(MANUFACTURER_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="test",
            password="123vc123a"
        )
        self.client.force_login(self.user)

    def test_retrieve_manufacturers_and_search(self):
        Manufacturer.objects.create(name="Test11", country="USA")
        Manufacturer.objects.create(name="Test22", country="USB")

        response = self.client.get(MANUFACTURER_URL)
        self.assertEqual(response.status_code, 200)
        manufacturers = Manufacturer.objects.all()
        self.assertEqual(
            list(response.context["manufacturer_list"]),
            list(manufacturers),
        )
        self.assertTemplateUsed(response, "taxi/manufacturer_list.html")

        response = self.client.get(MANUFACTURER_URL, {"name": "Test11"})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["manufacturer_list"])
        self.assertEqual(len(result), 1)

        response = self.client.get(MANUFACTURER_URL, {"name": ""})
        self.assertEqual(response.status_code, 200)
        result = list(response.context["manufacturer_list"])
        self.assertEqual(len(result), 2)
