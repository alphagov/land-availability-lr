'''
Setup:

pip install palettable==3.0.0
pip install requests_cache
export HMRC_USER=<username>
export HMRC_PASSWORD=<password>
'''
import time
import csv
import os
import json
import palettable

import requests_cache

from lr.models import Title
from django.core.management.base import BaseCommand

requests_cache.install_cache('hmrc_api')

class Command(BaseCommand):
    help = 'Given a uprn, works out what titles and polygons are associated'

    def add_arguments(self, parser):
        parser.add_argument('uprn_csv_filename', type=str)
        # use UPRN CSV until it is in the database

        parser.add_argument('uprn', type=str)

    def handle(self, *args, **options):
        uprn = options['uprn']

        addressbase_info = lookup_uprn_in_addressbase(uprn)[0]
        address_str = serialize_address(addressbase_info['address'])
        print('Uprn: {} {}'
              .format(uprn, address_str))

        titles = []
        groups_of_polygons = []
        for title in lookup_uprn_in_csv(
                options['uprn_csv_filename'], uprn):
            titles.append(title)
            title_obj = Title.objects.get(id=title)
            print('Title {} has {} polygons'.format(
                title, title_obj.polygons.count()))
            groups_of_polygons.append(
                (title, '{} {}'.format(uprn, address_str),
                 title_obj.polygons.all()))
        print(groups_of_polygons_to_geojson(groups_of_polygons))

def groups_of_polygons_to_geojson(groups_of_polygons):
    colours = palettable.colorbrewer.qualitative.Set1_9.hex_colors
    features = []
    for i, group_of_polygons in enumerate(groups_of_polygons):
        name, description, polygons = group_of_polygons
        colour = colours[i % len(colours)]
        features.extend(polygons_to_features(
            name, description, colour, polygons))

    geojson = {
        "type": "FeatureCollection",
        "features": features,
        }
    return json.dumps(geojson)

def polygons_to_geojson(name, description, colour, polygons):
    geojson = {
        "type": "FeatureCollection",
        "features": polygons_to_features(name, description, colour, polygons)
        }
    return json.dumps(geojson)

def polygons_to_features(name, description, colour, polygons):
    return [
        {
            "type": "Feature",
            "properties": {
                "name": str(name),
                "popupContent": str(description),
                "fill": colour,
                },
            "geometry": json.loads(polygon.geom.geojson)
        }
        for polygon in polygons
    ]

def serialize_address(address):
    # e.g. {'lines': ['10 Portal Road'],
    #       'town': 'Stafford',
    #       'county': 'Staffordshire',
    #       'postcode': 'ST16 3QR',
    #       'subdivision': {'code': 'GB-ENG', 'name': 'England'}
    #      }
    all_lines = []
    for key, value in address.items():
        if key == 'lines':
            all_lines.extend(value)
        elif key in ('subdivision', 'country'):
            continue
        else:
            all_lines.append(value)
    return ', '.join(all_lines)

def lookup_uprn_in_csv(uprn_csv_filename, uprn):
    with open(
            uprn_csv_filename,
            newline='', encoding=None) as csvfile:

        reader = csv.reader(csvfile, delimiter=',', quotechar='"')

        for count, row in enumerate(reader):
            if row[1] == uprn:
                title_id, uprn_id, add_or_update = row
                yield title_id

def lookup_uprn_in_addressbase(uprn=None):
    url = 'https://txm-al-demo.tax.service.gov.uk/v2/uk/addresses'
    # params e.g. ?uprn=200003273799'
    params = dict(uprn=uprn)
    # NB 'limit' causes 400 error
    headers = {'user-agent': 'gds-analyse-uprn'}
    auth = (os.environ['HMRC_USER'], os.environ['HMRC_PASSWORD'])
    requests_session = requests_cache.CachedSession('hmrc_api')
    requests_session.hooks = {'response': make_requests_throttle_hook(1.0)}
    response = requests_session.get(
        url, params=params, auth=auth, headers=headers)
    response.raise_for_status()
    return response.json()

def make_requests_throttle_hook(timeout=1.0):
    def hook(response, *args, **kwargs):
        if not getattr(response, 'from_cache', False):
            print('sleeping')
            time.sleep(timeout)
        return response
    return hook

