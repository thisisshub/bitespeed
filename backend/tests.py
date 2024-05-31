from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class IdentifyViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_email_only(self):
        data = {"email": "test@example.com"}
        response = self.client.post("/identify/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_phone_number_only(self):
        data = {"phoneNumber": "1234567890"}
        response = self.client.post("/identify/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_both_contacts(self):
        data = {"email": "test@example.com", "phoneNumber": "1234567890"}
        response = self.client.post("/identify/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_no_contacts(self):
        data = {}
        response = self.client.post("/identify/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
