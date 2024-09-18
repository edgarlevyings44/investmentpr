from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserRegistrationTest(APITestCase):

    def test_register_user(self):
        """
        Ensure we can register a new user.
        """
        url = reverse('register_user')
        data = {
            'username': 'testuser',
            'password': 'TestPass123',
            'email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_invalid_data(self):
        """
        Ensure registration fails with invalid data.
        """
        url = reverse('register_user')
        data = {
            'username': '',
            'password': '',
            'email': 'invalid-email'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)
        self.assertIn('email', response.data)

class UserTokenTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='TestPass123',
            email='test@example.com'
        )

    def test_obtain_token(self):
        """
        Ensure we can obtain a token with correct credentials.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'TestPass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_invalid_credentials(self):
        """
        Ensure token is not provided with invalid credentials.
        """
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'WrongPass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)