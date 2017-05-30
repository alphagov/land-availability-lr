from lr.models import Title, Uprn
from .importers import CSVImportCommand


class Command(CSVImportCommand):
    help = 'Import UPRNs from a CSV file'

    def process_row(self, row):
        title_id, uprn_id, add_or_update = row
        try:
            title = Title.objects.get(id=title_id)
        except Title.DoesNotExist:
            # print('Cannot add UPRN {0} - missing Title entry: {1}'
            #       .format(uprn_id, title_id))
            outcome = 'ignored - uprn does not match any Title'
        else:
            try:
                uprn = Uprn.objects.get(uprn=uprn_id)
                if uprn.title == title:
                    return 'unchanged'
                outcome = 'updated'
            except Uprn.DoesNotExist:
                uprn = Uprn()
                uprn.uprn = uprn_id
                outcome = 'created'

            uprn.title = title

            try:
                uprn.save()
            except Exception as e:
                print('Cannot add: {} - {}'.format(row, e))
                outcome = 'Error: could not save object'
        return outcome
