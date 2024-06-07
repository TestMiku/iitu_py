from django.core.management.base import BaseCommand, CommandError, CommandParser
from django.conf import settings
import pathlib
import logging
import datetime
import shutil

class Command(BaseCommand):
    
    def handle(self, *args, **options):
            
        db_path: pathlib.Path = pathlib.Path(settings.BASE_DIR/"db_for_website.sqlite3")

        if not db_path.exists():
            return None
        output_path: pathlib.Path = pathlib.Path("../db_backups/kartel")
        logging.info(f"Бэкап базы данных {db_path} в {output_path}.")
        
        filename = f"kartel-backup-{datetime.date.today().strftime('%d-%m-%Y')}.sqlite3"
        output_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(db_path, output_path / filename)
        logging.info(f"Сделан бэкап {filename}.")

    