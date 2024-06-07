import json
import pathlib
from datetime import datetime

from avh_services import read_json
from portal_avh.celery import app
from celery import shared_task
from .views import update_data_from_json, import_19_45, update_data_7_11_2
from calculator_emr.views import auto_import_bs, auto_import_1922
import os
from contract_report.views import import_adem_data
from Security_Department.scripts.EveryMonthsReportOil import main as script_main
import time
from  document_debts import services

def shedule_time(sheduled_time: datetime):
    now = datetime.now()

    if now >= sheduled_time:
        return True
    else:
        return False


@shared_task
def auto_updates():
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, hour=9)
    if now <= scheduled_time:
        try:
            update_data_from_json()
            return 'SUCESS'
        except Exception as e:
            return 'ERROR: ' + str(e)
    else:
        return 'Отменяем! Задача запланирована на ' + scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
@shared_task
def auto_updates_19_45():
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, hour=9)
    if now <= scheduled_time:
        try:
            import_19_45()
            return 'SUCESS'
        except Exception as e:
            return 'ERROR: ' + str(e)
    else:
        return 'Отменяем! Задача запланирована на ' + scheduled_time.strftime('%Y-%m-%d %H:%M:%S')
@shared_task
def auto_updates_7_11_2():
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, hour=8)
    if now <= scheduled_time:
        try:
            update_data_7_11_2()
            return 'SUCESS'
        except Exception as e:
            return 'ERROR: ' + str(e)
    else:
        return 'Отменяем! Задача запланирована на ' + scheduled_time.strftime('%Y-%m-%d %H:%M:%S')

@shared_task
def auto_updates_19_22():
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, hour=10)
    if now <= scheduled_time:
        try:
            auto_import_1922()
            return 'SUCESS'
        except Exception as e:
            return 'ERROR: ' + str(e)
    else:
        return 'Отменяем! Задача запланирована на ' + scheduled_time.strftime('%Y-%m-%d %H:%M:%S')

@shared_task
def auto_updates_for_emr():
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, hour=10)
    if now <= scheduled_time:
        try:
            auto_import_bs()
            return 'SUCESS'
        except Exception as e:
            return 'ERROR: ' + str(e)
    else:
        return 'Отменяем! Задача запланирована на ' + scheduled_time.strftime('%Y-%m-%d %H:%M:%S')

@shared_task
def test_celery():
    print('test_celery is running')
    path = os.listdir('/mnt/adem-otchet')
    return path





@shared_task
def read_and_read_json(filename: str | None = None, indent: int = 2,
                       **kwargs) -> None:  # path: PathLike, start: str, end: str, output_path: PathLike = "contract_report/adem",
    now = datetime.now()
    scheduled_time = datetime(now.year, now.month, now.day, hour=10)
    if now <= scheduled_time:
        path = "/mnt/adem-otchet/19_20.json"
        start = "colgroup"
        end = "c_invoice_id"
        output_path: os.PathLike = "contract_report/adem"
        output_path = pathlib.Path(output_path)
        output_path.mkdir(parents=True, exist_ok=True)
        with open(output_path / "19_20.json", "w", encoding="utf-8") as file:
            data = list(read_json(path, start, end))
            file.write("[")
            for i, row in enumerate(data):
                file.write(json.dumps(row, indent=indent, ensure_ascii=False, **kwargs))
                if i < len(data) - 1:  # Добавить запятую после каждого элемента, кроме последнего
                    file.write(",")
            file.write("]")
        time.sleep(30)
        # import_adem_data()

        services.import_data()
        return 'SUCСESS'
    else:
        return 'Отменяем! Задача запланирована на ' + scheduled_time.strftime('%Y-%m-%d %H:%M:%S')


# @shared_task
# def debt_on_doc_for_dima():
#     script_main()