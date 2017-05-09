from django.contrib.gis.geos import GEOSGeometry
from .importers import ShapefileImportCommand
from lr.models import LRPoly
import json
from datetime import datetime


class Command(ShapefileImportCommand):
    help = 'Import Land Registry Polygons from a *.shp file'

    def process_record(self, record):
        try:
            poly = LRPoly.objects.get(title=record.record[1])
            outcome = 'updated'
        except LRPoly.DoesNotExist:
            poly = LRPoly()
            outcome = 'created'
            poly.title = record.record[1]

        poly.insert = datetime.strptime(record.record[2], '%Y-%m-%dT%H:%M:%S')
        poly.update = datetime.strptime(record.record[3], '%Y-%m-%dT%H:%M:%S')
        poly.status = record.record[4]
        poly.geom = GEOSGeometry(
            json.dumps(record.shape.__geo_interface__), srid=27700)

        try:
            poly.save()
        except Exception as e:
            print('Could not add: {0}'.format(record.record))
            outcome = 'Error: could not save'
        return outcome
