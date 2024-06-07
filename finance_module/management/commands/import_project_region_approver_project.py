from django.core.management.base import BaseCommand, CommandError, CommandParser
from ... import models
from django.conf import settings

class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("path", default=settings.BASE_DIR / "finance_module/project-region-approver-project.json")

    def handle(self, *args, **options):
        models.ProjectRegionApproverProject.objects.all().delete()
        models.ProjectRegionApprover.objects.all().delete()
        
