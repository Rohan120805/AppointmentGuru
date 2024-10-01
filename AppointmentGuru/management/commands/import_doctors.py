import csv
from django.core.management.base import BaseCommand
from AppointmentGuru.models import Doctor

class Command(BaseCommand):
    help = 'Import doctors from doctors.csv'

    def handle(self, *args, **kwargs):
        with open('AppointmentGuru\management\commands\doctors.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                doctor = Doctor(
                    doctorName=row['doctorName'],
                    email=row['email'],
                    phoneNumber=row['phoneNumber'],
                    age=row['age'],
                    gender=row['gender'],
                    specialisation=row['specialisation'],
                    hospitalName=row['hospitalName'],
                    branch=row['branch'],
                    time=row['time'],
                    password=row['password']
                )
                doctor.save()
        self.stdout.write(self.style.SUCCESS('Successfully imported doctors'))