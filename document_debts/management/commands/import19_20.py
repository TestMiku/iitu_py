from django.core.management.base import BaseCommand, CommandError
from ... import services

class Command(BaseCommand):
    def handle(self, *args, **options):
        services.import_data_()