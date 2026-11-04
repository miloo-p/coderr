from django.urls import reverse
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

    def test_post_an_offer(self):
        response = self.client.post("/api/offers/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_offer_with_two_details(self):

        data = {
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
            ],
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/offers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_with_details_of_same_type(self):

        data = {
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
                    "title": "Basic Design",
                    "revisions": 3,
                    "delivery_time_in_days": 7,
                    "price": 110,
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
            ],
        }

        self.client.force_authenticate(user=self.user)
        response = self.client.post("/api/offers/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_offer_as_customer(self):
        self.customer = CoderrUser.objects.create_user(
            username="TestUserCustomer",
            email="example@mail.de",
            password="test123",
            type="customer",
        )
        self.client.force_authenticate(user=self.customer)
        response = self.client.post("/api/offers/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_a_single_offer(self):
        created = self.client.post("/api/offers/", self.data, format="json")
        url = reverse("offer-detail", kwargs={"pk": created.data["id"]})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["min_price"], 100)
        self.assertEqual(response.data["min_delivery_time"], 5)
        self.assertEqual(len(response.data["details"]), 3)
        self.assertEqual(set(response.data["details"][0].keys()), {"id", "url"})

    def test_get_a_single_offer_details(self):
        created = self.client.post("/api/offers/", self.data, format="json")
        url = reverse("offerdetail-infos", kwargs={"pk": created.data["details"][0]["id"]})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["price"], 100)
        self.assertEqual(response.data["offer_type"], "basic")

    def test_get_offers_while_not_authenticated(self):
        self.client.force_authenticate(user=None)
        url = reverse("offers")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_offer_while_not_authenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post("/api/offers/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_of_offers(self):
        self.client.force_authenticate(user=self.user)
        self.client.post("/api/offers/", self.data, format="json")
        response = self.client.get("/api/offers/")
        self.assertEqual(
            response.data["results"][0]["user_details"]["username"], self.user.username
        )

    def test_get_list_of_offers_with_pagination(self):
        self.client.force_authenticate(user=self.user)
        self.client.post("/api/offers/", self.data, format="json")
        self.client.post("/api/offers/", self.data, format="json")
        response = self.client.get("/api/offers/?page_size=1")
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 1)
