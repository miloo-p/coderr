from rest_framework import status
from rest_framework.test import APITestCase


class CoderrUserRegistrationTests(APITestCase):
    def test_create_coderruser_with_valid_data_returns_201(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self.client.post("/api/registration/", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_datacheck(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self.client.post("/api/registration/", data, format="json")
        self.assertEqual(set(response.data.keys()), {"token", "username", "email", "user_id"})

    def test_post_usernamecheck(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePassword",
            "type": "customer",
        }

        response = self.client.post("/api/registration/", data, format="json")
        self.assertEqual(response.data["username"], data["username"])

    def test_post_passwordcheck_nomatch(self):
        data = {
            "username": "exampleUsername",
            "email": "example@mail.de",
            "password": "examplePassword",
            "repeated_password": "examplePasswordXXX",
            "type": "customer",
        }

        response = self.client.post("/api/registration/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
