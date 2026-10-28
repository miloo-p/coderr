from rest_framework import status
from rest_framework.test import APITestCase

from .models import CoderrUser


class CoderrUserRegistrationTests(APITestCase):
    def setUp(self):

        self.data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

    def test_create_coderruser_with_valid_data_returns_201(self):

        response = self.client.post("/api/registration/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_datacheck(self):
        response = self.client.post("/api/registration/", self.data, format="json")
        self.assertEqual(set(response.data.keys()), {"token", "username", "email", "user_id"})

    def test_post_usernamecheck(self):
        response = self.client.post("/api/registration/", self.data, format="json")
        self.assertEqual(response.data["username"], self.data["username"])

    def test_post_passwordcheck_nomatch(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "NOMATCH",
            "type": "customer",
        }
        response = self.client.post("/api/registration/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_coderruser_with_dbentry_type(self):
        self.client.post("/api/registration/", self.data, format="json")
        user = CoderrUser.objects.get(username=self.data["username"])

        self.assertEqual(user.type, self.data["type"])

    def test_post_coderruser_pw_is_hashed(self):
        self.client.post("/api/registration/", self.data, format="json")
        user = CoderrUser.objects.get(username=self.data["username"])
        self.assertTrue(user.check_password(self.data["password"]))
        self.assertNotEqual(user.password, self.data["password"])

    def test_post_is_mail_already_in_use(self):
        CoderrUser.objects.create_user(
            username="TestUser",
            email="example@mail.de",
            password="test123",
            type="customer",
        )
        response = self.client.post("/api/registration/", self.data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
