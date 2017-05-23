from unittest import TestCase
import pytest
import json
from django.contrib.gis.geos import Point
from lr.models import Polygon, Title
from lr.serializers import PolygonCreationSerializer


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
