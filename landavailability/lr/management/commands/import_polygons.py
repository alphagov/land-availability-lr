from django.contrib.gis.geos import GEOSGeometry
from .importers import ShapefileImportCommand
from lr.models import Polygon, Title
import json
from datetime import datetime


class Command(ShapefileImportCommand):
    help = 'Import Land Registry Polygons from a *.shp file'

    def __init__(self, *kargs, **kwargs):
        self.db_empty_from_start = (
            not Polygon.objects.exists() and not Title.objects.exists())
        print('Optimizing because db starts empty: {}'.format(
              self.db_empty_from_start))
        self.polygon_ids = set()
        self.title_ids = set()
        ShapefileImportCommand(*kargs, **kwargs)

    def process_record(self, polygon_id, title_id, insert_date, update_date,
                       status, geometry):

        def create_polygon():
            poly = Polygon()
            self.polygon_ids.add(polygon_id)
            poly.id = polygon_id
            return poly
        if not self.db_empty_from_start or polygon_id in self.polygon_ids:
            try:
                poly = Polygon.objects.get(id=polygon_id)
                outcome = 'updated'
            except Polygon.DoesNotExist:
                poly = create_polygon()
                outcome = 'created'
        else:
            poly = create_polygon()
            outcome = 'created'

        def create_title():
            title = Title()
            title.id = title_id
            return title
        if not self.db_empty_from_start or title_id in self.title_ids:
            try:
                title = Title.objects.get(id=title_id)
            except Title.DoesNotExist:
                title = create_title()
        else:
            title = create_title()

        try:
            title.save()
        except Exception as e:
            print('Could not add title: {} {}'.format(title_id, e))
            outcome = 'Error: could not save'
            return outcome

        poly.title = title
        poly.insert = datetime.strptime(insert_date, '%Y-%m-%dT%H:%M:%S')
        poly.update = datetime.strptime(update_date, '%Y-%m-%dT%H:%M:%S')
        poly.status = status
        poly.geom = GEOSGeometry(
            json.dumps(geometry), srid=27700)

        try:
            poly.save()
        except Exception as e:
            print('Could not add: {} {}'.format(record.record, e))
            outcome = 'Error: could not save'
        return outcome
