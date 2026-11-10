from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import CoderrUser

from .models import Review


class ReviewTests(APITestCase):
    def setUp(self):
        self.business_user = CoderrUser.objects.create_user(
            username="TestBusiness", password="test123", type="business"
        )
        self.customer_user = CoderrUser.objects.create_user(
            username="TestCustomer", password="test123", type="customer"
        )
        self.client.force_authenticate(user=self.customer_user)
        self.url = reverse("reviews")
        self.data = {
            "business_user": self.business_user.id,
            "rating": 4,
            "description": "Alles war toll!",
        }

    def test_post_review_as_customer(self):
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["reviewer"], self.customer_user.id)

    def test_post_second_review_for_same_business(self):
        self.client.post(self.url, self.data, format="json")
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)

    def test_post_review_as_business(self):
        self.client.force_authenticate(user=self.business_user)
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_review_for_customer_user(self):
        self.data["business_user"] = self.customer_user.id
        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_reviews_filtered_and_ordered(self):
        other_business = CoderrUser.objects.create_user(
            username="OtherBusiness", password="test123", type="business"
        )
        self.client.post(self.url, self.data, format="json")
        self.client.post(
            self.url,
            {"business_user": other_business.id, "rating": 5, "description": "Top!"},
            format="json",
        )
        response = self.client.get(self.url, {"business_user_id": self.business_user.id})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.url, {"ordering": "-rating"})
        self.assertEqual(response.data[0]["rating"], 5)

    def create_review_and_url(self):
        response = self.client.post(self.url, self.data, format="json")
        return reverse("review-detail", kwargs={"pk": response.data["id"]})

    def test_patch_review_as_reviewer(self):
        url = self.create_review_and_url()
        response = self.client.patch(url, {"rating": 5}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["rating"], 5)
        self.assertEqual(response.data["description"], "Alles war toll!")

    def test_patch_review_with_forbidden_field(self):
        url = self.create_review_and_url()
        response = self.client.patch(url, {"rating": 5, "business_user": 999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_review_as_other_customer(self):
        url = self.create_review_and_url()
        other_customer = CoderrUser.objects.create_user(
            username="OtherCustomer", password="test123", type="customer"
        )
        self.client.force_authenticate(user=other_customer)
        response = self.client.patch(url, {"rating": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_as_reviewer(self):
        url = self.create_review_and_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_as_other_customer(self):
        url = self.create_review_and_url()
        other_customer = CoderrUser.objects.create_user(
            username="OtherCustomer", password="test123", type="customer"
        )
        self.client.force_authenticate(user=other_customer)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Review.objects.count(), 1)
