import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


class LandRegistryUserAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@…', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class TestVOACreateView(LandRegistryUserAPITestCase):
    @pytest.mark.django_db
    def test_voa_view_create_object(self):
        url = reverse('lr-detail', kwargs={'uprn': '00260500013008'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
