import pytest
from unittest import TestCase
from django.contrib.gis.geos import GEOSGeometry
from lr.models import LRPoly, Uprn
from datetime import datetime


class TestLandModel(TestCase):
    @pytest.mark.django_db
    def test_lrpoly_model_creation(self):
        lrpoly = LRPoly()
        lrpoly.title = 'A6523948'
        lrpoly.insert = datetime.now()
        lrpoly.update = datetime.now()
        lrpoly.status = 'A'

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

        lrpoly.geom = GEOSGeometry(geometry, srid=27700)
        lrpoly.save()

        self.assertEqual(LRPoly.objects.count(), 1)

    @pytest.mark.django_db
    def test_uprn_model_creation(self):
        lrpoly = LRPoly()
        lrpoly.title = 'A6523948'
        lrpoly.insert = datetime.now()
        lrpoly.update = datetime.now()
        lrpoly.status = 'A'

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

        lrpoly.geom = GEOSGeometry(geometry, srid=27700)
        lrpoly.save()

        self.assertEqual(LRPoly.objects.count(), 1)

        uprn = Uprn()
        uprn.title = lrpoly
        uprn.uprn = "0031535421432"
        uprn.save()

        self.assertEqual(Uprn.objects.count(), 1)
