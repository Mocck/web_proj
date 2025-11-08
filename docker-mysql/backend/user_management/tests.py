from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import User


class UserManagementTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        # register
        data = {"username": "testuser", "email": "test@example.com", "password": "pass123"}
        resp = self.client.post(reverse('um_register'), data, format='json')
        self.assertEqual(resp.status_code, 201)
        self.assertIn('token', resp.data)

        # login
        login_data = {"username_or_email": "testuser", "password": "pass123"}
        resp2 = self.client.post(reverse('um_login'), login_data, format='json')
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('token', resp2.data)

    def test_users_list_requires_auth(self):
        # unauthenticated should be 401 or 403
        resp = self.client.get(reverse('um_users'))
        self.assertIn(resp.status_code, (401, 403))

    def test_list_after_login(self):
        # create and login
        User.objects.create(username='u1', email='u1@example.com', password='pbkdf2...')
        data = {"username": "t2", "email": "t2@example.com", "password": "pass123"}
        reg = self.client.post(reverse('um_register'), data, format='json')
        self.assertEqual(reg.status_code, 201)
        token = reg.data['token']['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        resp = self.client.get(reverse('um_users'))
        self.assertEqual(resp.status_code, 200)
from django.test import TestCase

# Create your tests here.
