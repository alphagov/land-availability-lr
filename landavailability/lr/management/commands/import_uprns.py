import sys

from lr.models import Title, Uprn
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import UPRNs from a CSV file'

    def handle(self, *args, **options):
        # we need to start from a blank uprn table, otherwise out-of-date
        # links in the uprn-title m2m will not get deleted.
        num_uprns = Uprn.objects.count()
        if num_uprns > 0:
            response = input('There are {} uprns in the db that need deleting.'
                             ' Continue? (y/n) >'.format(num_uprns))
            if response.lower() != 'y':
                sys.exit()
            Uprn.objects.all().delete()

        super(Command, self).handle(*args, **options)

    def process_row(self, row):
        title_id, uprn_id, add_or_update = row
        try:
            title = Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            # print('Cannot add UPRN {0} - missing Title entry: {1}'
            #       .format(uprn_id, title_id))
            outcome = 'ignored - uprn does not match any title in the db'
        else:
            try:
                uprn = Uprn.objects.get(uprn=uprn_id)
                outcome = 'added'
            except Uprn.DoesNotExist:
                uprn = Uprn()
                uprn.uprn = uprn_id
                try:
                    uprn.save()
                except Exception as e:
                    print('Cannot save: {} - {}'.format(row, e))
                    return 'Error: could not save new uprn'

                outcome = 'added (also created uprn)'

            uprn.titles.add(title)

            try:
                uprn.save()
            except Exception as e:
                print('Cannot add: {} - {}'.format(row, e))
                outcome = 'Error: could not save uprn link'
        return outcome
