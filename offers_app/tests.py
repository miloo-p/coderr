from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import CoderrUser


class OfferTests(APITestCase):
    def setUp(self):

        self.user = CoderrUser.objects.create_user(
            username="TestUser",
            email="example@mail.de",
            password="test123",
            type="business",
        )
        self.client.force_authenticate(user=self.user)

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

    def test_post_an_Offer(self):
        response = self.client.post("/api/offers/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
