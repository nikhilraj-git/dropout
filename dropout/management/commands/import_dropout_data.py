import csv
from django.core.management.base import BaseCommand
from dropout.models import StudentDropout
import datetime

class Command(BaseCommand):
    help = 'Import dropout data from CSV'

    def handle(self, *args, **kwargs):
        with open('dropout_analysis_dummy.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Convert dropout_year to a date
                dropout_date = datetime.date(int(row['dropout_year']), 1, 1)
                
                StudentDropout.objects.create(
                    school_name=row['school_name'],
                    area=row['area'],
                    gender=row['gender'],
                    caste=row['caste'],
                    age=int(row['age']),
                    standard=row['standard'],
                    date_of_dropout=dropout_date,
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully.'))