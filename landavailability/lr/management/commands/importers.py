from collections import defaultdict
from pprint import pprint

from django.core.management.base import BaseCommand
import csv
import shapefile


class CSVImportCommand(BaseCommand):
    help = 'Import data from a CSV file'

    def __init__(self, skip_header=False, encoding=None):
        self.skip_header = skip_header
        self.encoding = encoding

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def process_row(self, row):
        pass

    def handle(self, *args, **options):
        csv_file_name = options.get('csv_file')

        if csv_file_name:
            with open(
                    csv_file_name,
                    newline='', encoding=self.encoding) as csvfile:

                reader = csv.reader(csvfile, delimiter=',', quotechar='"')

                if self.skip_header:
                    next(reader)

                outcome_counts = defaultdict(int)
                for row in reader:
                    outcome = self.process_row(row)
                    outcome_counts[outcome or 'processed'] += 1
                    pprint(dict(outcome_counts))


class ShapefileImportCommand(BaseCommand):
    help = 'Import data from a *.shp file'

    def add_arguments(self, parser):
        parser.add_argument('shp_filename', type=str, nargs='+')

    def process_record(self, record):
        pass

    def handle(self, *args, **options):
        shp_filenames = options['shp_filename']

        outcome_counts = defaultdict(int)
        for shp_filename in shp_filenames:
            self.process_shapefile(shp_filename,
                                   outcome_counts)

    def process_shapefile(self, shp_filename, outcome_counts):
        print('Processing shapefile {}'.format(shp_filename))
        shp_reader = shapefile.Reader(shp_filename)
        for record in shp_reader.iterShapeRecords():
            if record.shape.shapeType == shapefile.NULL:
                outcome_counts['no shapefile'] += 1
                continue
            outcome = self.process_record(record)
            outcome_counts[outcome or 'processed'] += 1
            pprint(dict(outcome_counts))
