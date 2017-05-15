import time
from collections import defaultdict

# pip install numpy==1.12.1
import numpy as np

from django.core.management.base import BaseCommand
import shapefile
from django.contrib.gis.geos import GEOSGeometry
from lr.models import LRPoly
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Check Land Registry Polygons in *.shp files'

    def add_arguments(self, parser):
        parser.add_argument('shp_filename', type=str, nargs='+')

    def handle(self, *args, **options):
        shp_filenames = options['shp_filename']

        outcomes = defaultdict(list)
        polygons_by_title = defaultdict(list)
        start_time = time.time()
        for shp_filename in shp_filenames:
            self.process_shapefile(shp_filename,
                                   outcomes,
                                   polygons_by_title,
                                   start_time)

    def process_shapefile(self, shp_filename, outcomes, polygons_by_title,
                          start_time):
        print('Processing shapefile {}'.format(shp_filename))
        shp_reader = shapefile.Reader(shp_filename)
        for count, record in enumerate(shp_reader.iterShapeRecords()):
            # "Every title, whether freehold or leasehold, has at least one
            #  index polygon."
            # Record:
            # [15386807, # Poly_ID
            #  'DN232592', # Title_No
            #  '2002-01-16T00:00:00', '2002-01-16T00:00:00', 'A']
            poly_id = record.record[0]
            title = record.record[1]
            if record.shape.shapeType == shapefile.NULL:
                outcome = 'no shapefile'
            else:
                polygons_by_title[title].append(record.record)
                outcome = 'processed'
            outcomes[outcome or 'processed'].append(poly_id)
            if count % 100000 == 0:
                print_polygon_title_stats(polygons_by_title)
                print_outcomes_and_rate(outcomes, start_time)
        print_polygon_title_stats(polygons_by_title)
        print_outcomes_and_rate(outcomes, start_time)

def print_polygon_title_stats(polygons_by_title):
    num_polygons_by_title = dict(
        (title, len(polygons))
        for title, polygons in polygons_by_title.items())
    num_polygons = sum(num_polygons_by_title.values())
    num_titles = len(polygons_by_title)
    print('Polygons: {} Titles: {} Polygons/title: {:.2f}'.format(
        num_polygons, num_titles, float(num_polygons) / num_titles))
    # freq distribution
    num_polygons_by_title_ = \
        [float(num) for num in num_polygons_by_title.values()]
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
    hist = np.histogram(num_polygons_by_title_, bins=bins)
    print(np.stack((hist[1][:-1], hist[0])))
    print('>20: {} Max: {}'.format(
        sum(1 for num_polygons in num_polygons_by_title.values()
            if num_polygons > 20),
        max(num_polygons_by_title.values())))

def print_outcomes_and_rate(outcomes, start_time):
    total_count = sum([len(rows) for rows in outcomes.values()])
    rate_per_hour = total_count / (time.time() - start_time) * 60 * 60
    for outcome, rows in outcomes.items():
        print('{} {} e.g. {}'.format(len(rows), outcome, rows[0]))
    print('Count: {} Rate: {:.0f}/hour'
          .format(total_count, round(rate_per_hour, -3)))
