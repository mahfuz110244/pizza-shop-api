import json
from .models import Pizza, Order
from user.models import Customer
from django.urls import reverse
from rest_framework.test import APITestCase


class ShopAPITestCase(APITestCase):
    url = reverse("user:login")

    def setUp(self):
        self.username = "+8801520103197"
        self.name = "Mahfuzur Rahman Khan"
        self.email = "mahfuzku11@gmail.com"
        self.password = "bs23"
        data = {
            'username': self.username,
            'name': self.name,
            'email': self.email
        }
        self.user = Customer.objects.create_user(self.password, **data)
        self.pizza_data_one = {
            'name': "Indian BBQ Pizza",
            'brand': "Indian",
            'price': 500,
            'weight': 1,
            'availability': "yes"
        }
        self.pizza_data_two = {
            'name': "American BBQ Pizza",
            'brand': "American",
            'price': 1000,
            'weight': 1,
            'availability': "yes"
        }
        self.pizza1 = Pizza.objects.create(**self.pizza_data_one)
        self.pizza2 = Pizza.objects.create(**self.pizza_data_two)
        self.order_data_one = {
            "pizza": self.pizza1,
            "customer": self.user,
            "order_price": 1000,
            "quantity": 2,
            "address": "Mohammadpur",
            "latitude": 104.33,
            "longitude": 566778.99
        }
        self.order1 = Order.objects.create(**self.order_data_one)
        self.jwt_token = self.get_jwt_token()

    def get_jwt_token(self):
        url = reverse("user:login")
        data = {"phone": self.username, "password": self.password}
        response = self.client.post(url, data, format='json')
        response_data = json.loads(response.content)
        return response_data['jwt_token']

    def test_get_pizza_list_api(self):
        url = reverse("shop:pizza_list")
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_get_pizza_detail_api_valid_data(self):
        url = reverse("shop:pizza_detail", kwargs={"pk": self.pizza1.pk})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_get_pizza_detail_api_invalid_data(self):
        url = reverse("shop:pizza_detail", kwargs={"pk": 10})
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_order_post_api_without_jwt_token(self):
        url = reverse("shop:order_list")
        data = {
            "pizza": self.pizza1.id,
            "customer": self.user.id,
            "order_price": 1000,
            "quantity": 2,
            "address": "Mohammadpur",
            "location":
                {"lat": 104.33, "lng": 566778.99}
        }
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(401, response.status_code)
        # self.assertTrue("err" in json.loads(response.content))

    def test_order_post_api_with_valid_data(self):
        url = reverse("shop:order_list")
        data = {
            "pizza": self.pizza1.id,
            "customer": self.user.id,
            "order_price": 1000,
            "quantity": 2,
            "address": "Mohammadpur",
            "location":
                {"lat": 104.33, "lng": 566778.99}
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(200, response.status_code)

    def test_order_post_api_with_err_msg_invalid_pizza(self):
        url = reverse("shop:order_list")
        data = {
            "pizza": 1000,
            "customer": self.user.id,
            "order_price": 1000,
            "quantity": 2,
            "address": "Mohammadpur",
            "location":
                {"lat": 104.33, "lng": 566778.99}
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(400, response.status_code)
        print(json.loads(response.content))
        self.assertTrue("err" in json.loads(response.content))

    def test_order_list_get_api_valid_data(self):
        url = reverse("shop:order_list")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_order_detail_get_api_invalid_data(self):
        url = reverse("shop:order_detail", kwargs={"pk": 10000})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer  ' + self.jwt_token)
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)
