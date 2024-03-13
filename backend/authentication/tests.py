from enum import Enum
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.apps import AuthenticationConfig
from authentication.models import User


class ReverseViewName(str, Enum):
    AUTHENTICATION = AuthenticationConfig.name
    LOGIN = f'{AUTHENTICATION}:login'
    LOGOUT = f'{AUTHENTICATION}:logout'
    USER_LIST = f'{AUTHENTICATION}:user-list'
    USER_DETAIL = f'{AUTHENTICATION}:user-detail'


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpassword',
        )
    
    def test_login(self):
        response = self.client.post(
            reverse(ReverseViewName.LOGIN),
            data={
                'username': 'testuser',
                'password': 'testpassword',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)

    def test_logout(self):
        response = self.client.get(
            reverse(ReverseViewName.LOGOUT),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserTestCase(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='superuser',
            email='supertest@test.com',
            password='testpassword',
        )
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpassword',
        )
    
    def test_user_list(self):
        self.client.force_authenticate(user=self.superuser)
        response = self.client.get(
            reverse(ReverseViewName.USER_LIST),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_user_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(ReverseViewName.USER_DETAIL, args=[self.user.id]),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
    
    def test_user_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse(ReverseViewName.USER_DETAIL, args=[self.user.id]),
            data={
                'username': 'newusername',
                'email': 'test1@test.com',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'newusername')
        self.assertEqual(response.data['email'], 'test1@test.com')
    
    def test_user_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse(ReverseViewName.USER_DETAIL, args=[self.user.id]),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
