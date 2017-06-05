import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.gis.geos import GEOSGeometry
from lr.models import Polygon, Uprn, Title
from datetime import datetime


class LandRegistryUserAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_user(
            username='test', email='test@…', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class LandRegistryAdminAPITestCase(APITestCase):
    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_superuser(
            username='test', email='test@…', password='top_secret')
        token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)


class TestUprnLookupView(LandRegistryUserAPITestCase):
    @pytest.mark.django_db
    def test_lr_view_lookup_uprn(self):
        # Create a Title
        title = Title(id='A6523948')
        title.save()

        # Ceate a Polygon and set the Title
        poly = Polygon()
        poly.id = 1234
        poly.title = title
        poly.insert = datetime(2004, 11, 8)
        poly.update = datetime(2004, 11, 9)
        poly.status = 'A'

        geometry = """
            {"coordinates": [
                [
                    [592272.735, 343444.716],
                    [592272.532, 343445.693],
                    [592273.469, 343445.927],
                    [592273.604, 343445.958],
                    [592280.779, 343447.745],
                    [592281.121, 343447.834],
                    [592281.265, 343447.867],
                    [592281.606, 343447.955],
                    [592289.051, 343449.809],
                    [592289.378, 343449.891],
                    [592289.407, 343449.898],
                    [592289.61, 343448.92],
                    [592274.257, 343445.087],
                    [592273.98, 343445.02],
                    [592272.735, 343444.716]
                ]
            ], "type": "Polygon"}
        """

        poly.geom = GEOSGeometry(geometry, srid=27700)
        poly.save()

        # Create the Uprn and set the Title
        uprn = Uprn()
        uprn.uprn = "0031535421432"
        uprn.save()
        uprn.titles.add(title)

        url = reverse('uprn-detail', kwargs={'uprn': '0031535421432'})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['titles'][0]['id'], 'A6523948')
        self.assertEqual(
            response.json()['titles'][0]['polygons'][0]['geom']['type'],
            'Polygon')
        self.assertEqual(response.json()['uprn'], '0031535421432')
        self.assertEqual(
            response.json()['titles'][0]['polygons'][0]['status'], 'A')
        self.assertEqual(
            response.json()['titles'][0]['polygons'][0]['insert'],
            '2004-11-08T00:00:00')
        self.assertEqual(
            response.json()['titles'][0]['polygons'][0]['update'],
            '2004-11-09T00:00:00')


class TestPolygonCreateView(LandRegistryAdminAPITestCase):
    @pytest.mark.django_db
    def test_lr_polygon_create_view(self):
        url = reverse('polygon-create')
        data = {
            "id": 12345,
            "title": "ABC123",
            "insert": "2004-11-08T00:00:00",
            "update": "2004-11-09T00:00:00",
            "status": "C",
            "geom": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-0.22341515058230163, 52.93036769987315],
                        [-0.22039561538021543, 52.93215130879717],
                        [-0.21891135174799967, 52.93122765287705],
                        [-0.22193998154995934, 52.92945074233686],
                        [-0.22341515058230163, 52.93036769987315]
                    ]
                ]
            },
            "srid": 27700
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Polygon.objects.count(), 1)
        self.assertEqual(Title.objects.count(), 1)


class TestUprnCreateView(LandRegistryAdminAPITestCase):
    @pytest.mark.django_db
    def test_lr_uprn_create_view(self):
        url = reverse('uprn-create')
        data = {
            "uprn": 12345,
            "title": "ABC123"
        }

        title = Title(id='ABC123')
        title.save()

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Uprn.objects.count(), 1)

        uprn_saved = Uprn.objects.first()
        self.assertEqual(uprn_saved.titles.all()[0].id, 'ABC123')
