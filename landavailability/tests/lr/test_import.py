import datetime

import pytest
from unittest import TestCase
from lr.models import Polygon
from lr.management.commands.import_polygons import Command as PolygonCommand


class TestImportPolygons(TestCase):
    @pytest.mark.django_db
    def test_import_one_polygon(self):
        geometry_geojson = \
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
        PolygonCommand().process_record(
            37133011, 'NK314862',
            '2004-11-08T00:00:00', '2004-11-09T00:00:00', 'A',
            geometry_geojson)

        poly = Polygon.objects.get(id=37133011)
        self.assertEqual(poly.title.id, 'NK314862')
        self.assertEqual(poly.insert, datetime.datetime(2004, 11, 8))
        self.assertEqual(poly.update, datetime.datetime(2004, 11, 9))
        self.assertEqual(poly.status, 'A')
