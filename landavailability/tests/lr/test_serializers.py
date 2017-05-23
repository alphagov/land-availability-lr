from unittest import TestCase
import pytest
import json
from lr.models import Polygon, Title, Uprn
from lr.serializers import PolygonCreationSerializer, UprnCreationSerializer


class TestPolygonSerializer(TestCase):
    @pytest.mark.django_db
    def test_polygon_creation_serializer_create_object(self):
        json_payload = """
            {
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
        """

        data = json.loads(json_payload)
        serializer = PolygonCreationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Polygon.objects.count(), 1)
        self.assertEqual(Title.objects.count(), 1)


class TestUprnSerializer(TestCase):
    @pytest.mark.django_db
    def test_uprn_creation_serializer_create_object(self):
        json_payload = """
            {
                "uprn": 12345,
                "title": "ABC123"
            }
        """

        title = Title(id="ABC123")
        title.save()

        data = json.loads(json_payload)
        serializer = UprnCreationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        serializer.save()
        self.assertEqual(Uprn.objects.count(), 1)
        self.assertEqual(Title.objects.count(), 1)

    @pytest.mark.django_db
    def test_uprn_creation_serializer_create_object_invalid_title(self):
        json_payload = """
            {
                "uprn": 12345,
                "title": "ABC123"
            }
        """

        data = json.loads(json_payload)
        serializer = UprnCreationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
