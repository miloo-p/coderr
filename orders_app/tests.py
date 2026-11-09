from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import CoderrUser


# Create your tests here.
class OrderTests(APITestCase):
    def setUp(self):

        self.business_user = CoderrUser.objects.create_user(
            username="TestBusiness",
            email="example@mail.de",
            password="test123",
            type="business",
        )

        self.customer_user = CoderrUser.objects.create_user(
            username="TestCustomer",
            email="example@mail.de",
            password="test123",
            type="customer",
        )

        self.data = {
            "title": "Grafikdesign-Paket",
            "image": None,
            "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
            "details": [
                {
                    "title": "Basic Design",
                    "revisions": 2,
                    "delivery_time_in_days": 5,
                    "price": 100,
                    "features": ["Logo Design", "Visitenkarte"],
                    "offer_type": "basic",
                },
                {
                    "title": "Standard Design",
                    "revisions": 5,
                    "delivery_time_in_days": 7,
                    "price": 200,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier"],
                    "offer_type": "standard",
                },
                {
                    "title": "Premium Design",
                    "revisions": 10,
                    "delivery_time_in_days": 10,
                    "price": 500,
                    "features": ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
                    "offer_type": "premium",
                },
            ],
        }

        self.client.force_authenticate(user=self.business_user)
        response = self.client.post("/api/offers/", self.data, format="json")
        self.offer_detail_id = response.data["details"][0]["id"]
        self.client.force_authenticate(user=self.customer_user)

    def test_post_orders(self):
        url = reverse("orders")
        response = self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["price"], 100)
        self.assertEqual(response.data["business_user"], self.business_user.id)

    def test_post_orders_by_an_business_user(self):
        self.client.force_authenticate(user=self.business_user)

        url = reverse("orders")
        response = self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_orders_with_no_data(self):
        url = reverse("orders")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
