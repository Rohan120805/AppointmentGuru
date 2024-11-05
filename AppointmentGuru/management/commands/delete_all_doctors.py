from django.core.management.base import BaseCommand
from App1.AppointmentGuru.models import Doctor

class Command(BaseCommand):
    help = 'Delete all doctors from the database'

    def handle(self, *args, **kwargs):
        Doctor.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all doctors'))