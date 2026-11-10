from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import CoderrUser
from offers_app.models import Offer
from reviews_app.models import Review


class BaseInfoTests(APITestCase):
    def setUp(self):
        self.url = reverse("base-info")

    def test_base_info_on_empty_database(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"review_count": 0, "average_rating": 0, "business_profile_count": 0, "offer_count": 0},
        )

    def test_base_info_counts_and_rounds(self):
        business = CoderrUser.objects.create_user(
            username="Anna", password="test123", type="business"
        )
        CoderrUser.objects.create_user(username="Ben", password="test123", type="business")
        Offer.objects.create(user=business, title="Website", description="Eine Website")
        for number, rating in enumerate([4, 5, 5]):
            customer = CoderrUser.objects.create_user(
                username=f"Kunde{number}", password="test123", type="customer"
            )
            Review.objects.create(
                reviewer=customer, business_user=business, rating=rating, description="Gut"
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["review_count"], 3)
        self.assertEqual(response.data["average_rating"], 4.7)
        self.assertEqual(response.data["business_profile_count"], 2)
        self.assertEqual(response.data["offer_count"], 1)
