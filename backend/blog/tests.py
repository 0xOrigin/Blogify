from enum import Enum
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.apps import BlogConfig
from django.contrib.auth import get_user_model
from blog.models import Post

User = get_user_model()


class ReverseViewName(str, Enum):
    BLOG = BlogConfig.name
    POST_LIST = f'{BLOG}:post-list'
    POST_DETAIL = f'{BLOG}:post-detail'


class PostTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1',
            email='test1@test.com',
            password='testpassword',
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.user,
            created_at=timezone.now(),
        )
    
    def test_post_list(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(ReverseViewName.POST_LIST),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_detail(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse(ReverseViewName.POST_DETAIL, kwargs={'pk': self.post.pk}),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_create(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(ReverseViewName.POST_LIST),
            data={
                'title': 'New Post',
                'content': 'This is a new post.',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author']['id'], str(self.user.id))
    
    def test_post_update(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.put(
            reverse(ReverseViewName.POST_DETAIL, kwargs={'pk': self.post.pk}),
            data={
                'title': 'Updated Post',
                'content': 'This is an updated post.',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Post')
    
    def test_post_delete(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            reverse(ReverseViewName.POST_DETAIL, kwargs={'pk': self.post.pk}),
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
