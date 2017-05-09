from lr.models import LRPoly, Uprn
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import UPRNs from a CSV file'

    def process_row(self, row):
        print(row)

        try:
            poly = LRPoly.objects.get(title=row[0])
        except LRPoly.DoesNotExist:
            print(
                'Cannot add UPRN {0} - Missing Title entry: {1}'
                .format(row[1], row[0]))
        else:
            try:
                uprn = Uprn.objects.get(uprn=row[1])
            except Uprn.DoesNotExist:
                uprn = Uprn()
                uprn.uprn = row[1]

            uprn.title = poly

            try:
                uprn.save()
            except Exception as e:
                print('Could not add: {0}'.format(row))
