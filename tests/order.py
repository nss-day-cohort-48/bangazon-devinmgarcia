from bangazonapi.models.payment import Payment
import json
from rest_framework import status
from rest_framework.test import APITestCase
from bangazonapi.models import Order


class OrderTests(APITestCase):
    def setUp(self) -> None:
        """
        Create a new account and create sample category
        """
        url = "/register"
        data = {"username": "steve", "password": "Admin8*", "email": "steve@stevebrownlee.com",
                "address": "100 Infinity Way", "phone_number": "555-1212", "first_name": "Steve", "last_name": "Brownlee"}
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.token = json_response["token"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a product category
        url = "/productcategories"
        data = {"name": "Sporting Goods"}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        # Create a product
        url = "/products"
        data = { "name": "Kite", "price": 14.99, "quantity": 60, "description": "It flies high", "category_id": 1, "location": "Pittsburgh" }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Create a payment type
        url = "/paymenttypes"
        data = {
                "merchant_name": "Paypal",
                "account_number": "000000000000",
                "expiration_date": "2023-12-12",
                "create_date": "2020-12-12"
                }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')
        self.payment_type_id = response.data['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_product_to_order(self):
        """
        Ensure we can add a product to an order.
        """
        # Add product to order
        url = "/cart"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was added
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["id"], 1)
        self.assertEqual(json_response["size"], 1)
        self.assertEqual(len(json_response["lineitems"]), 1)
        self.assertEqual(json_response['payment_type'], None)


    def test_remove_product_from_order(self):
        """
        Ensure we can remove a product from an order.
        """
        # Add product
        self.test_add_product_to_order()

        # Remove product from cart
        url = "/cart/1"
        data = { "product_id": 1 }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Get cart and verify product was removed
        url = "/cart"
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.get(url, None, format='json')
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["size"], 0)
        self.assertEqual(len(json_response["lineitems"]), 0)

    def test_add_payment_type(self):
        """
        Ensure we can add a payment type to an order.
        """

        order = Order()
        order.customer_id = 1
        order.payment_type_id = None
        order.created_date = "2021-09-03"
        order.save()

        url = f'/orders/{order.id}'

        data = {
            "customer": order.customer_id,
            "payment_type_id": self.payment_type_id,
            "created_date": order.created_date
        }

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(url, None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        json_response = json.loads(response.content)
        self.assertEqual(json_response["payment_type"]['url'], "http://testserver/paymenttypes/1")

    # TODO: New line item is not added to closed order