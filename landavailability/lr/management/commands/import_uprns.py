from lr.models import LRPoly, Uprn
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import UPRNs from a CSV file'

    def process_row(self, row):
        try:
            poly = LRPoly.objects.get(title=row[0])
        except LRPoly.DoesNotExist:
            print(
                'Cannot add UPRN {0} - missing Title entry: {1}'
                .format(row[1], row[0]))
            outcome = 'ignored - uprn does not match any Title'
        else:
            try:
                uprn = Uprn.objects.get(uprn=row[1])
                outcome = 'updated'
            except Uprn.DoesNotExist:
                uprn = Uprn()
                uprn.uprn = row[1]
                outcome = 'created'

            uprn.title = poly

            try:
                uprn.save()
            except Exception as e:
                print('Could not add: {0}'.format(row))
                outcome = 'Error: could not save object'
        return outcome
