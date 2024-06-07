import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Exists, OuterRef, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render

from document_debts.models import DebtDocument, DebtPermanentFilter, DebtSupplier

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
    "nepredorigdo",
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


@login_required
def index(request, filter_id=None):
    suppliers = DebtSupplier.objects.all()

    # Если есть глобальный фильтр
    # Делаем фильтр через документы и получаем их связанные контрагенты так как фильтр указывается для документа
    global_filter = None
    if filter_id:
        # Убираю исключенные документы у которого нет связанного контрагента
        documents = DebtDocument.objects.filter(debt_supplier=OuterRef("id"))

        # Убираю исключенные документы их списка ислюченных документов
        exclude_filter = json.load(
            open("document_debts/exclusion_list.json", "r", encoding="utf-8")
        )
        for key in exclude_filter:
            documents = documents.exclude(**{f"{key}__in": exclude_filter[key]})
        documents = documents.exclude(dateinvoiced__lt=datetime(2021, 1, 1))

        # Фильтрация указанная в глобальном фильтре
        global_filter = DebtPermanentFilter.objects.filter(id=filter_id)
        if global_filter and global_filter[0].value:
            filters = {}
            for field, values in global_filter[0].value.items():
                filters[f"{field}__in"] = values
            documents = documents.filter(**filters)

        # Получаем связанные контрагенты
        suppliers_id = documents.values("debt_supplier").distinct()
        suppliers = DebtSupplier.objects.filter(id__in=suppliers_id).distinct()

    # Поиск
    if "search" in request.GET and request.GET["search"]:
        search_query = request.GET["search"]
        suppliers = suppliers.filter(
            Q(debt_documents__documentno__icontains=search_query)
            | Q(too__icontains=search_query)
            | Q(postavshik__icontains=search_query)
            | Q(bin__icontains=search_query)
        )

    # Фильтрация
    min_number = request.GET.get("min_summ", -999000000000)
    max_number = request.GET.get("max_summ", 999000000000)
    only_changed_suppliers = request.GET.get("only_changed_suppliers", "")
    if min_number and max_number:
        suppliers = suppliers.filter(
            debts_total_unclosedbalance__range=(min_number, max_number)
        )

    if only_changed_suppliers:
        suppliers = suppliers.exclude(last_unclosedbalance_change=0)

    # Исключаем контрагенты у которых нет связанных документов
    suppliers = suppliers.filter(
        Exists(DebtDocument.objects.filter(debt_supplier_id=OuterRef("id")))
    )

    # Уникализация
    suppliers = suppliers.distinct()

    # Сортировка (по умолчанию по сумме задолженности по убыванию)
    if "sorted_by" in request.GET and request.GET["sorted_by"]:
        sorted_field = request.GET["sorted_by"]
        suppliers = suppliers.order_by(sorted_field)
    else:
        suppliers = suppliers.order_by("-debts_total_unclosedbalance")

    # Основные данные по контрагентам и их документам
    docs = DebtDocument.objects.filter(debt_supplier__in=suppliers)

    docs_count = docs.count()
    docs_summ = docs.aggregate(Sum("unclosedbalance"))["unclosedbalance__sum"]

    suppliers_count = (len(suppliers),)
    suppliers_total_sum = suppliers.aggregate(Sum("debts_total_unclosedbalance"))[
        "debts_total_unclosedbalance__sum"
    ]

    # Пагинация
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(suppliers, 50)  # По 10 элементов на страницу
    try:
        suppliers = paginator.page(page_number)
    except PageNotAnInteger:
        suppliers = paginator.page(1)
    except EmptyPage:
        suppliers = paginator.page(paginator.num_pages)
    prev_page_number = page_number - 1
    next_page_number = page_number + 1
    page_range = [
        i
        for i in range(
            max(1, page_number - 5), min(paginator.num_pages, page_number + 5) + 1
        )
    ]
    more_than_10 = True if paginator.num_pages > 10 else False

    context = {
        # Основные данные
        "fields": fields,
        "suppliers": suppliers,
        # Дополнительные данные
        "suppliers_count": suppliers_count,
        "suppliers_total_sum": suppliers_total_sum,
        "docs_count": docs_count,
        "docs_summ": docs_summ,
        # Фильтры
        "filter_name": global_filter[0].name if global_filter else None,
        "filter_data": global_filter[0] if global_filter else None,
        "global_filters": DebtPermanentFilter.objects.all(),
        # Пагинация
        "paginator": paginator,
        "page_number": page_number,
        "prev_page_number": prev_page_number,
        "next_page_number": next_page_number,
        "page_range": page_range,
        "more_than_10": more_than_10,
    }
    return render(request, "document_debts/index.html", context)


def permanent_filter(request, filter_id):
    # context = {
    #     "filter_name": filter_name,
    #     "suppliers": suppliers,
    #     "suppliers_count": len(suppliers_QuerySet),
    #     "suppliers_total_sum": suppliers_QuerySet.aggregate(
    #         Sum("debts_total_unclosedbalance")
    #     )["debts_total_unclosedbalance__sum"],
    #     "fields": fields,
    #     "paginator": paginator,
    #     "page_number": page_number,
    #     "global_filters": DebtPermanentFilter.objects.all(),
    #     "prev_page_number": page_number - 1,
    #     "next_page_number": page_number + 1,
    #     "page_range": [
    #         i
    #         for i in range(
    #             max(1, page_number - 5), min(paginator.num_pages, page_number + 5) + 1
    #         )
    #     ],
    #     "more_than_10": True if paginator.num_pages > 10 else False,
    # }

    return render(request, "document_debts/index.html")


@login_required
def docs(request, filter_id=None):
    documents = None

    # Если есть глобальный фильтр
    filter_name = None
    filter_body = DebtPermanentFilter.objects.filter(id=filter_id)
    if filter_body and filter_body[0].value:
        filters = {}
        for field, values in filter_body[0].value.items():
            filters[f"{field}__in"] = values
        documents = DebtDocument.objects.filter(**filters, unclosedbalance__gte=1000)
        filter_name = filter_body[0].name
    else:
        documents = DebtDocument.objects.filter(unclosedbalance__gte=1000)

    # Есть исключенные документы. Их обязательно надо убрать. Какие есть исключения указаны в папке exclusion_list
    exclude_filter = json.load(
        open("document_debts/exclusion_list.json", "r", encoding="utf-8")
    )
    for key in exclude_filter:
        documents = documents.exclude(**{f"{key}__in": exclude_filter[key]})
    documents = documents.exclude(dateinvoiced__lt=datetime(2021, 1, 1))

    # Фильтры
    filter_search = request.GET.get("search", None)
    filter_min_summ = request.GET.get("min_summ", None)
    filter_max_summ = request.GET.get("max_summ", None)
    filter_only_changed_suppliers = request.GET.get("only_changed_suppliers", None)
    only_changed_suppliers_up = request.GET.get("only_changed_suppliers_up", None)
    only_changed_suppliers_down = request.GET.get("only_changed_suppliers_down", None)

    if filter_search:
        documents = documents.filter(
            Q(documentno__icontains=filter_search)
            | Q(too__icontains=filter_search)
            | Q(postavshik__icontains=filter_search)
            | Q(bin__icontains=filter_search)
        )

    if filter_min_summ:
        documents = documents.filter(unclosedbalance__gte=filter_min_summ)

    if filter_max_summ:
        documents = documents.filter(unclosedbalance__lte=filter_max_summ)

    if only_changed_suppliers_up:
        documents = documents.filter(last_unclosedbalance_change__gt=0)

    if only_changed_suppliers_down:
        documents = documents.filter(last_unclosedbalance_change__lt=0)

    if filter_only_changed_suppliers == "on":
        documents = documents.exclude(last_unclosedbalance_change=0)
        documents = documents.exclude(last_unclosedbalance_change=None)

    # Для того что бы документы не повторялись получаем только уникальные значения
    documents = documents.distinct()

    # Сортировка если есть то опционально сортируем. По умолчанию по уменьшению суммы незакрытого остатка
    if "sorted_by" in request.GET and request.GET["sorted_by"]:
        sorted_field = request.GET["sorted_by"]
        documents = documents.order_by(sorted_field)
    else:
        documents = documents.order_by("-unclosedbalance")

    # Получаем данные для показа общих данных
    #   - Общие данные по контрагентам
    suppliers_id = documents.values_list("debt_supplier_id", flat=True)
    suppliers = DebtSupplier.objects.filter(pk__in=suppliers_id).distinct()
    suppliers_count = len(suppliers)
    suppliers_total_sum = sum(
        supplier["debts_total_unclosedbalance"]
        for supplier in suppliers.values("debts_total_unclosedbalance")
    )
    #   - Общие данные по документам
    debt_documents_count = len(documents)
    debt_documents_total_sum = documents.aggregate(
        total_unclosed_balance=Sum("unclosedbalance")
    )["total_unclosed_balance"]

    # Пагинация
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(documents, 50)  # По 10 элементов на страницу
    try:
        documents = paginator.page(page_number)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)
    prev_page_number = page_number - 1
    next_page_number = page_number + 1
    page_range = [
        i
        for i in range(
            max(1, page_number - 5), min(paginator.num_pages, page_number + 5) + 1
        )
    ]
    more_than_10 = True if paginator.num_pages > 10 else False

    context = {
        # основное
        "fields": fields,
        "debt_documents": documents,
        # те данные что показывают общие кол-во и сумма
        "debt_documents_count": debt_documents_count,
        "debt_documents_total_sum": debt_documents_total_sum,
        "suppliers_count": suppliers_count,
        "suppliers_total_sum": suppliers_total_sum,
        # еданные о глобальном фильтре
        "filter_name": filter_name,
        "filter_id": filter_id,
        "global_filters": DebtPermanentFilter.objects.all(),
        # для пагинации
        "paginator": paginator,
        "page_number": page_number,
        "prev_page_number": prev_page_number,
        "next_page_number": next_page_number,
        "page_range": page_range,
        "more_than_10": more_than_10,
    }

    return render(request, "document_debts/documents_table.html", context)


def pbi_19_20(request):
    file_path = "contract_report/adem/19_20.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = {"result": data}
    return JsonResponse(data)


def pbi_filters(request):
    file_path = "document_debts/exclusion_list.json"
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    data = {"result": data}
    return JsonResponse(data)
