#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import datetime
import logging
import mimetypes
import os
import pathlib
import shutil
import sys
import time


def make_db_backup() -> None:
    backup_time: datetime.timedelta = datetime.timedelta(hours=6)
    db_path: pathlib.Path = pathlib.Path("db.sqlite3")
    if not db_path.exists():
        return None
    output_path: pathlib.Path = pathlib.Path("../db_backups")
    logging.info(f"Бэкап базы данных {db_path} в {output_path}.")
    latest = max(output_path.glob("*"), key=lambda x: x.stat().st_ctime, default=None)
    
    if not latest or (difference := time.time() - latest.stat().st_ctime) > backup_time.total_seconds():
        filename = f"db-backup-{datetime.date.today().strftime('%d-%m-%Y')}.sqlite3"
        output_path.mkdir(parents=True, exist_ok=True)
        shutil.copy(db_path, output_path / filename)
        logging.info(f"Сделан бэкап {filename}.")
    else:
        logging.info(f"Бэкап будет сделан через {datetime.datetime.fromtimestamp(backup_time.total_seconds()) - datetime.datetime.fromtimestamp(difference)}.")

def make_kartel_backup() -> None:
    
    db_path: pathlib.Path = pathlib.Path("db_for_website.sqlite3")
    if not db_path.exists():
        return None
    output_path: pathlib.Path = pathlib.Path("../db_backups/kartel")
    logging.info(f"Бэкап базы данных {db_path} в {output_path}.")
    
    filename = f"kartel-backup-{datetime.date.today().strftime('%d-%m-%Y')}.sqlite3"
    output_path.mkdir(parents=True, exist_ok=True)
    shutil.copy(db_path, output_path / filename)
    logging.info(f"Сделан бэкап {filename}.")
   
def main():
    mimetypes.init()
    mimetypes.add_type("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", ".xlsx")
    logging.basicConfig(
        filename="logs.txt", filemode="a", level=logging.INFO, encoding="utf-8"
    )
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal_avh.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
