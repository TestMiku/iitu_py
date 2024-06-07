import sqlite3
import time

from asgiref.sync import sync_to_async
from django.db import transaction

global_time = int(time.time() * 1000)


def time_difference():
    global global_time
    current_time = int(time.time() * 1000)
    difference = current_time - global_time
    global_time = current_time
    return difference


import asyncio
import json
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

from django.db import transaction
from django.db.models.query import QuerySet
from django.utils.timezone import make_aware

from document_debts.models import (
    DebtChangesHistory,
    DebtDocument,
    DebtImportError,
    DebtSupplier,
)


@transaction.atomic
def remove_unnecessary_connections():
    documents_to_update = DebtDocument.objects.filter(
        unclosedbalance__lt=1000,
    )
    documents_to_update |= DebtDocument.objects.filter(
        dateinvoiced__lt=datetime(2021, 1, 1)
    )

    exclude_filter = json.load(
        open("document_debts/exclusion_list.json", "r", encoding="utf-8")
    )
    for key, value_list in exclude_filter.items():
        documents_to_update |= DebtDocument.objects.filter(**{f"{key}__in": value_list})

    # print(documents_to_update.count())
    documents_to_update.update(debt_supplier=None)
    return 0


def update_suppliers():
    total_summ = 0
    suppliers = DebtSupplier.objects.all()
    for supplier in suppliers:
        supplier.last_unclosedbalance_change = (
            supplier.get_last_unclosedbalance_change()
        )
        supplier.debts_total_unclosedbalance = (
            supplier.get_debts_total_unclosedbalance()
        )
        supplier.save()
        total_summ += supplier.debts_total_unclosedbalance
        # print(f"Поставщик {supplier.bin} обновлен")
    # print(f"Общая сумма долгов по поставщикам: {total_summ}")


debt_suppliers = {}
debt_documents = {}


fields = [
    "colgroup",
    "documentno",
    "name",
    "dateinvoiced",
    "nscheta",
    "dogovor",
    "datascheta",
    "coment",
    "status",
    "too",
    "postavshik",
    "bin",
    "accountno",
    "bank",
    "totallines",
    "payamt1c",
    "notpayamt1c",
    "otvzakup",
    "utverditel",
    "gruppa_proekrov",
    "valyuta",
    "napravlenie",
    "error_txt",
    "sumpaid",
    "dname",
    "docstatus",
    "paydate1c",
    "icname",
    "chname",
    "createdby",
    "nomdocument1",
    "datadoc",
    "komment",
    "nepredorigdoc",
    "isattached",
    "factnumdoc",
    "doc_number",
    "site",
    "c_currency_id",
    "refundamt",
    "daterefund",
    "actdocno",
    "docserviceact",
    "docdate",
    "dateprocessed",
    "quantity",
    "amount",
    "region",
    "invoiceamount",
    "security_agreed",
    "refundamtkzt",
    "totallineskzt",
    "payamt1ckzt",
    "notpayamt1ckzt",
    "notpayamt1ckztcross",
    "unclosedbalance",
    "c_invoice_id",
]


def update_lists():
    global debt_suppliers, debt_documents
    debt_suppliers = {supplier.bin: supplier for supplier in DebtSupplier.objects.all()}
    debt_documents = {
        doc.documentno: {
            "unclosedbalance": doc.unclosedbalance,
            "debt_document": doc,
        }
        for doc in DebtDocument.objects.all()
    }


def set_data(item):
    # Проверяю типы данных переменных и преобразую их в нужный формат
    for field in [
        "dateinvoiced",
        "datascheta",
        "daterefund",
        "docdate",
        "dateprocessed",
        "paydate1c",
    ]:
        item[field] = check_data(item.get(field, None), datetime)

    # Если нет БИН-а то нет смысла дальше продолжать так как это обез поле
    debt_supplier = None
    if bin := item.get("bin"):
        debt_supplier = debt_suppliers.get(bin)
        if not debt_supplier:
            debt_supplier = DebtSupplier.objects.create(
                bin=bin, postavshik=item.get("postavshik"), name=item.get("name")
            )
    else:
        return 0

    # Обновляю документ если он есть
    if item.get("documentno") == None:
        return 0

    debt_document_from_dict = debt_documents.get(item.get("documentno"))
    if debt_document_from_dict:
        debt_document = debt_document_from_dict["debt_document"]

        # если сумма незакрытого остатка изменился то создаю историю
        if item.get("unclosedbalance") != debt_document_from_dict["unclosedbalance"]:
            old_obj = DebtDocument.objects.get(pk=debt_document.pk)
            old = get_dict(old_obj)
            for key in fields:
                if hasattr(debt_document, key):
                    setattr(debt_document, key, item.get(key))

            debt_document.last_unclosedbalance_change = (
                item.get("unclosedbalance") - debt_document_from_dict["unclosedbalance"]
            )
            debt_document.debt_supplier = debt_supplier
            debt_document.save()
            new = get_dict(debt_document)
            DebtChangesHistory.objects.create(
                debt_document=debt_document, old=old, new=new
            )

        # если не измениля то я по любому изменяю так как есть и другие изменения
        else:
            for key in fields:
                if hasattr(debt_document, key):
                    setattr(debt_document, key, item.get(key))

            debt_document.debt_supplier = debt_supplier
            debt_document.save()

    # Если нет документа то создаю его
    else:
        debt_document = DebtDocument.objects.create(**item, debt_supplier=debt_supplier)

    # Обновить список документов
    debt_documents[debt_document.documentno] = {
        "unclosedbalance": debt_document.unclosedbalance,
        "debt_document": debt_document,
    }

    debt_supplier.save()

    # Обновляю список контрагентов
    debt_suppliers[debt_supplier.bin] = debt_supplier


def loop_process(data):
    global debt_suppliers, debt_documents
    for item in data:
        try:
            set_data(item)
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                # Попробуйте еще раз
                set_data(item)
            else:
                print(f"SQLite Operational Error: {e}")

        except Exception as e:
            pass


def get_dict(obj):
    return {
        field: (
            getattr(obj, field).strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(getattr(obj, field), datetime)
            else str(getattr(obj, field))
        )
        for field in fields
    }


def check_data(data, datatype):
    if datatype in (int, float):
        try:
            return datatype(data)
        except (ValueError, TypeError):
            return 0
    elif datatype == datetime:
        try:
            naive_datetime = datetime.fromisoformat(data) if data else None
            aware_datetime = make_aware(naive_datetime) if naive_datetime else None
            return aware_datetime
        except (ValueError, TypeError):
            return None
    else:
        return data


def import_data_():
    data = []
    try:
        with open("contract_report/adem/19_20.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        print("File not found or invalid JSON format")
        return 0

    time_difference()

    update_lists()
    loop_process(data)

    # print(f"Обработка данных завершена за {time_difference()} миллисекунд")


def import_data():
    import_data_()
    remove_unnecessary_connections()
    update_suppliers()


# from document_debts.services import import_data, update_suppliers, remove_unnecessary_connections
# import_data()
