import csv
from django.core.management.base import BaseCommand
from dropout.models import StudentDropout

class Command(BaseCommand):
    help = 'Import dropout data from CSV'

    def handle(self, *args, **kwargs):
        with open('dropout_analysis_dummy.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                StudentDropout.objects.create(
                    school_name=row['school_name'],
                    area=row['area'],
                    gender=row['gender'],
                    caste=row['caste'],
                    age=int(row['age']),
                    standard=row['standard'],
                    dropout_year=int(row['dropout_year']),
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))
