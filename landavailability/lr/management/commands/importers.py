from collections import defaultdict
import time

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
                start_time = time.time()
                for count, row in enumerate(reader):
                    outcome = self.process_row(row)
                    outcome_counts[outcome or 'processed'] += 1
                    print_outcomes_and_rate(count, outcome_counts, start_time)


class ShapefileImportCommand(BaseCommand):
    help = 'Import data from a *.shp file'

    def add_arguments(self, parser):
        parser.add_argument('shp_filename', type=str, nargs='+')

    def process_record(self, record):
        pass

    def handle(self, *args, **options):
        shp_filenames = options['shp_filename']

        outcome_counts = defaultdict(int)
        start_time = time.time()
        for shp_filename in shp_filenames:
            self.process_shapefile(shp_filename,
                                   outcome_counts,
                                   start_time)

    def process_shapefile(self, shp_filename, outcome_counts, start_time):
        print('Processing shapefile {}'.format(shp_filename))
        shp_reader = shapefile.Reader(shp_filename)
        for count, record in enumerate(shp_reader.iterShapeRecords()):
            if record.shape.shapeType == shapefile.NULL:
                outcome_counts['no shapefile'] += 1
                continue
            outcome = self.process_record(record)
            outcome_counts[outcome or 'processed'] += 1
            print_outcomes_and_rate(count, outcome_counts, start_time)


def print_outcomes_and_rate(count, outcome_counts, start_time):
    if count % 100 == 0:
        total_count = sum(outcome_counts.values())
        rate_per_hour = total_count / (time.time() - start_time) * 60 * 60
        print(dict(outcome_counts), end=' ')
        print('Count: {} Rate: {:.0f}/hour'
              .format(total_count, round(rate_per_hour, -3)))
