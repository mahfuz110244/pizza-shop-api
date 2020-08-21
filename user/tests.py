import json
from .models import Customer
from django.urls import reverse
from rest_framework.test import APITestCase


class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("user:login")

    def setUp(self):
        self.username = "+8801520103197"
        self.name = "Mahfuzur Rahman Khan"
        self.email = "mahfuzku11@gmail.com"
        self.password = "bs23"
        self.data = {
            'username': self.username,
            'name': self.name,
            'email': self.email
        }
        self.user = Customer.objects.create_user(self.password, **self.data)

    def test_login_without_password(self):
        data = {"phone": self.username}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(401, response.status_code)

    def test_login_with_wrong_password(self):
        data = {"phone": self.username, "password": 'wrong_password'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(401, response.status_code)

    def test_login_with_valid_data(self):
        data = {"phone": self.username, "password": self.password}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(200, response.status_code)

    def test_login_with_valid_data_token(self):
        data = {"phone": self.username, "password": self.password}
        response = self.client.post(self.url, data, format='json')
        self.assertTrue("jwt_token" in json.loads(response.content))


class UserDetailsAPIViewTestCase(APITestCase):
    url = reverse("user:user_detail")

    def setUp(self):
        self.username = "+8801520103197"
        self.name = "Mahfuzur Rahman Khan"
        self.email = "mahfuzku11@gmail.com"
        self.password = "bs23"
        self.data = {
            'username': self.username,
            'name': self.name,
            'email': self.email
        }
        self.user = Customer.objects.create_user(self.password, **self.data)
        self.jwt_token = self.get_jwt_token()

    def get_jwt_token(self):
        url = reverse("user:login")
        data = {"phone": self.username, "password": self.password}
        response = self.client.post(url, data, format='json')
        response_data = json.loads(response.content)
        return response_data['jwt_token']

    def test_user_details_get_api_without_jwt_token(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_user_details_get_api_with_valid_jwt_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    def test_user_details_patch_api(self):
        data = {
            "name": "Mr Khan",
            "current_location": {
                "lat": 137216764.34,
                "lng": 327748278.56
            }
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.patch(self.url, data, format='json')
        self.assertEqual(200, response.status_code)
        self.assertTrue("msg" in json.loads(response.content))
