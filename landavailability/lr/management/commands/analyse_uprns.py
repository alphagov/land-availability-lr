import time
from collections import defaultdict
import csv
import operator

# pip install numpy==1.12.1
import numpy as np

from django.core.management.base import BaseCommand
from . import print_outcomes_and_rate


class Command(BaseCommand):
    help = 'Check a Land Registry Uprn-Title lookup csv file'

    def add_arguments(self, parser):
        parser.add_argument('csv_filename', type=str)

    def handle(self, *args, **options):
        csv_file_name = options['csv_filename']

        with open(
                csv_file_name,
                newline='', encoding=None) as csvfile:

            reader = csv.reader(csvfile, delimiter=',', quotechar='"')

            outcomes = defaultdict(list)
            uprns_by_title = defaultdict(list)
            titles_by_uprn = defaultdict(list)
            start_time = time.time()
            for count, row in enumerate(reader):
                outcome = self.process_row(row, uprns_by_title, titles_by_uprn)
                outcomes[outcome or 'processed'].append(row)
                if count % 50000 == 0:
                    print_outcomes_and_rate(outcomes, start_time)
                    print_uprn_title_stats(uprns_by_title, titles_by_uprn)
                    print('\n')
            print_outcomes_and_rate(outcomes, start_time)
            print_uprn_title_stats(uprns_by_title, titles_by_uprn)

    def process_row(self, row, uprns_by_title, titles_by_uprn):
        title_id, uprn_id, add_or_update = row
        uprns_by_title[title_id].append(uprn_id)
        titles_by_uprn[uprn_id].append(title_id)
        return 'processed'

def print_uprn_title_stats(uprns_by_title, titles_by_uprn):
    num_uprns_by_title = dict(
        (title, len(uprns))
        for title, uprns in uprns_by_title.items())
    num_titles_by_uprn = dict(
        (uprn, len(titles))
        for uprn, titles in titles_by_uprn.items())
    num_uprns = sum(num_uprns_by_title.values())
    num_titles = len(uprns_by_title)
    print('Uprns: {} Titles: {}'.format(
        num_uprns, num_titles))
    # freq distribution
    def print_freq_dist(value_counts, max_bin=10):
        value_counts_float = \
            [float(num) for num in value_counts.values()]
        bins = range(1, max_bin + 2)
        hist = np.histogram(value_counts_float, bins=bins)
        print(np.stack((hist[1][:-1], hist[0])))
        print('>{}: {} Max: {}'.format(
            max_bin,
            sum(1 for num_values in value_counts.values()
                if num_values > 20),
            max(value_counts.items(), key=operator.itemgetter(1))))
    print('Number of uprns per title: (average {:.2f})'.format(
        float(num_uprns) / num_titles))
    print_freq_dist(num_uprns_by_title)
    print('Number of titles per uprn: (average {:.2f})'.format(
        float(num_titles) / num_uprns))
    print_freq_dist(num_titles_by_uprn)
