from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from auth_app.models import CoderrUser
from orders_app.models import Order


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

    def test_post_orders_as_an_business_user(self):
        self.client.force_authenticate(user=self.business_user)

        url = reverse("orders")
        response = self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_orders_with_no_data(self):
        url = reverse("orders")
        response = self.client.post(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_orders_as_an_business_user(self):
        url = reverse("orders")
        self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.client.force_authenticate(user=self.business_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_orders_as_an_unrelated_user(self):
        self.silent_user = CoderrUser.objects.create_user(
            username="SilentBusiness",
            email="example@mail.de",
            password="test123",
            type="business",
        )
        url = reverse("orders")
        self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.client.force_authenticate(user=self.silent_user)
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_patch_order_status_by_creator(self):
        url = reverse("orders")
        response = self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.client.force_authenticate(user=self.business_user)
        url = reverse("orders-detail", kwargs={"pk": response.data["id"]})
        response = self.client.patch(url, {"status": "completed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "completed")

    def test_patch_order_status_by_different_user(self):
        self.different_user = CoderrUser.objects.create_user(
            username="differentBusiness",
            email="example@mail.de",
            password="test123",
            type="business",
        )
        url = reverse("orders")
        response = self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.client.force_authenticate(user=self.different_user)
        url = reverse("orders-detail", kwargs={"pk": response.data["id"]})
        response = self.client.patch(url, {"status": "completed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_order_with_invalid_data_by_creator(self):
        url = reverse("orders")
        response = self.client.post(url, {"offer_detail_id": self.offer_detail_id}, format="json")
        self.client.force_authenticate(user=self.business_user)
        url = reverse("orders-detail", kwargs={"pk": response.data["id"]})
        response = self.client.patch(url, {"status": "completed", "price": 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_order_as_staff(self):
        staff_user = CoderrUser.objects.create_user(
            username="StaffUser", password="test123", type="business", is_staff=True
        )
        response = self.client.post(
            reverse("orders"), {"offer_detail_id": self.offer_detail_id}, format="json"
        )
        self.client.force_authenticate(user=staff_user)
        url = reverse("orders-detail", kwargs={"pk": response.data["id"]})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_delete_order_as_business_user(self):
        response = self.client.post(
            reverse("orders"), {"offer_detail_id": self.offer_detail_id}, format="json"
        )
        self.client.force_authenticate(user=self.business_user)
        url = reverse("orders-detail", kwargs={"pk": response.data["id"]})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Order.objects.count(), 1)

    def test_order_counts(self):
        response = self.client.post(
            reverse("orders"), {"offer_detail_id": self.offer_detail_id}, format="json"
        )
        count_url = reverse("order-count", kwargs={"business_user_id": self.business_user.id})
        completed_url = reverse(
            "completed-order-count", kwargs={"business_user_id": self.business_user.id}
        )
        self.assertEqual(self.client.get(count_url).data["order_count"], 1)

        self.client.force_authenticate(user=self.business_user)
        detail_url = reverse("orders-detail", kwargs={"pk": response.data["id"]})
        self.client.patch(detail_url, {"status": "completed"}, format="json")
        self.assertEqual(self.client.get(count_url).data["order_count"], 0)
        self.assertEqual(self.client.get(completed_url).data["completed_order_count"], 1)

    def test_order_count_for_non_business_user(self):
        url = reverse("order-count", kwargs={"business_user_id": self.customer_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
