from django.contrib.gis.geos import GEOSGeometry
from .importers import ShapefileImportCommand
from lr.models import Polygon, Title
import json
from datetime import datetime


class Command(ShapefileImportCommand):
    help = 'Import Land Registry Polygons from a *.shp file'

    def process_record(self, record):
        polygon_id, title, insert_date, update_date, status = record.record
        try:
            poly = Polygon.objects.get(id=polygon_id)
            outcome = 'updated'
        except Polygon.DoesNotExist:
            poly = Polygon()
            outcome = 'created'
            poly.id = polygon_id

        try:
            title = Title.objects.get(id=title)
        except Title.DoesNotExist:
            title = Title()
            title.id = title

        try:
            title.save()
        except Exception as e:
            print('Could not add title: {} {}'.format(title, e))
            outcome = 'Error: could not save'
            return outcome

        poly.title = title
        poly.insert = datetime.strptime(insert_date, '%Y-%m-%dT%H:%M:%S')
        poly.update = datetime.strptime(update_date, '%Y-%m-%dT%H:%M:%S')
        poly.status = status
        poly.geom = GEOSGeometry(
            json.dumps(record.shape.__geo_interface__), srid=27700)

        try:
            poly.save()
        except Exception as e:
            print('Could not add: {} {}'.format(record.record, e))
            outcome = 'Error: could not save'
        return outcome
